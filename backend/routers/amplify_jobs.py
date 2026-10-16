import io
import json
import logging
import zipfile
import hashlib
from datetime import datetime, timezone
from pathlib import PureWindowsPath
from typing import Literal
from uuid import UUID
from xml.etree.ElementTree import ParseError

import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, ConfigDict, ValidationError, field_serializer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AmplifyJob
from backend.routers.amplify import require_local_request
from backend.routers.workflow_runs import require_transition
from backend.services import amplify_service
from backend.services.external_extraction_service import _docx_paragraphs


logger = logging.getLogger("kt_planner.amplify")
router = APIRouter(prefix="/api/v1/transitions/{transition_id}/amplify-jobs", tags=["Amplify planning jobs"])
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_BUNDLE_CHARS = 80_000


class WorkflowReceipt(BaseModel):
    accepted: Literal[True]
    workflow_id: Literal[167]
    project_id: Literal[77]
    run_id: UUID
    status: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    transition_id: str
    status: str
    source_files: list[dict]
    remote_run_id: str | None
    response: dict | None
    error: str | None
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_timestamp(self, value: datetime):
        return value.replace(tzinfo=timezone.utc).isoformat() if value.tzinfo is None else value.isoformat()


def extract_source(filename: str, content: bytes) -> str:
    suffix = PureWindowsPath(filename).suffix.lower()
    if suffix in (".txt", ".md", ".json", ".vtt", ".csv"):
        return content.decode("utf-8-sig")
    if suffix in (".docx", ".xlsx"):
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            if sum(item.file_size for item in archive.infolist()) > 20 * 1024 * 1024:
                raise ValueError("Expanded Office document exceeds 20 MB")
    if suffix == ".docx":
        return "\n".join(text for text, _style in _docx_paragraphs(io.BytesIO(content)))
    if suffix == ".xlsx":
        import openpyxl
        workbook = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        try:
            lines = []
            count = 0
            for sheet in workbook:
                lines.append(f"Worksheet: {sheet.title}")
                for row in sheet.iter_rows(values_only=True):
                    count += 1
                    if count > 5000:
                        raise ValueError("Workbook exceeds 5,000 rows; split it before upload")
                    lines.append(" | ".join("" if value is None else str(value) for value in row))
                    if sum(map(len, lines)) > MAX_BUNDLE_CHARS:
                        raise ValueError("Workbook text exceeds the source limit; split it before upload")
            return "\n".join(lines)
        finally:
            workbook.close()
    if suffix == ".pdf":
        import fitz
        try:
            with fitz.open(stream=content, filetype="pdf") as document:
                if len(document) > 200:
                    raise ValueError("PDF exceeds 200 pages")
                return "\n".join(f"Page {index + 1}\n{page.get_text()}" for index, page in enumerate(document))
        except fitz.FileDataError as exc:
            raise ValueError("PDF is invalid or unreadable") from exc
    raise ValueError("Supported formats: TXT, MD, JSON, VTT, CSV, DOCX, XLSX and text-based PDF")


@router.get("", response_model=list[JobResponse])
def list_jobs(transition_id: str, request: Request, db: Session = Depends(get_db)):
    require_local_request(request)
    require_transition(transition_id, db)
    return db.query(AmplifyJob).filter_by(transition_id=transition_id).order_by(AmplifyJob.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(transition_id: str, job_id: UUID, request: Request, db: Session = Depends(get_db)):
    require_local_request(request)
    require_transition(transition_id, db)
    job = db.get(AmplifyJob, str(job_id))
    if job is None or job.transition_id != transition_id:
        raise HTTPException(status_code=404, detail="Amplify job not found for this KT")
    return job


def read_source_bundle(files: list[UploadFile], instructions: str) -> tuple[str, list[dict]]:
    if not 1 <= len(files) <= 10:
        raise HTTPException(status_code=422, detail="Upload between 1 and 10 source files")
    sources = []
    texts = []
    for upload in files:
        filename = PureWindowsPath(upload.filename or "").name
        if not filename or len(filename) > 255 or "\n" in filename or "\r" in filename or any(source["filename"].casefold() == filename.casefold() for source in sources):
            raise HTTPException(status_code=422, detail="Each source needs a distinct filename")
        content = upload.file.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            raise HTTPException(status_code=422, detail=f"{filename} exceeds 5 MB")
        try:
            text = extract_source(filename, content).strip()
        except (ValueError, OSError, zipfile.BadZipFile, KeyError, ParseError) as exc:
            logger.warning("Source extraction failed for %s: %s", filename, type(exc).__name__)
            raise HTTPException(status_code=422, detail=f"Could not extract {filename}: {exc}") from exc
        if not text:
            raise HTTPException(status_code=422, detail=f"{filename} has no readable text. Scanned PDFs need OCR before upload")
        sources.append({"filename": filename, "bytes": len(content), "characters": len(text), "sha256": hashlib.sha256(content).hexdigest()})
        texts.append(f"BEGIN SOURCE {filename}\n{text}\nEND SOURCE {filename}")
        if sum(map(len, texts)) + len(instructions) > MAX_BUNDLE_CHARS:
            raise HTTPException(status_code=422, detail="Combined extracted sources exceed 80,000 characters; split the documents")
    bundle = f"Planning instructions from user:\n{instructions}\n\n" + "\n\n".join(texts)
    if len(bundle) > MAX_BUNDLE_CHARS:
        raise HTTPException(status_code=422, detail="Combined source bundle exceeds 80,000 characters")
    return bundle, sources


@router.post("", response_model=JobResponse, status_code=201)
def start_job(
    transition_id: str,
    request: Request,
    request_id: UUID = Form(...),
    instructions: str = Form(default="", max_length=5000),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    require_local_request(request)
    require_transition(transition_id, db)
    existing = db.get(AmplifyJob, str(request_id))
    if existing:
        if existing.transition_id != transition_id:
            raise HTTPException(status_code=409, detail="Request ID belongs to another KT")
        return existing
    bundle, sources = read_source_bundle(files, instructions)
    try:
        if not amplify_service.get_token():
            raise HTTPException(status_code=503, detail="Configure a Workflow access token first")
    except (OSError, RuntimeError, UnicodeError) as exc:
        logger.error("Amplify credential unlock failed: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Could not unlock Amplify credentials; configure the token again") from exc
    job = AmplifyJob(id=str(request_id), transition_id=transition_id, source_bundle=bundle, source_files=sources)
    db.add(job)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.get(AmplifyJob, str(request_id))
        if existing and existing.transition_id == transition_id:
            return existing
        raise
    try:
        response = amplify_service.submit_workflow(transition_id, bundle)
        token = amplify_service.get_token()
        body = response.text.replace(token, "[REDACTED]") if token else response.text
        if len(body) > 1_000_000:
            job.status = "response_error"
            job.error = "Amplify response exceeded 1 MB; inspect Amplify run history before retrying"
        else:
            try:
                data = json.loads(body)
            except ValueError:
                data = {"message": body[:2000]}
            job.response = data if isinstance(data, dict) else {"result": data}
            if response.is_success:
                try:
                    receipt = WorkflowReceipt.model_validate(job.response)
                except ValidationError:
                    job.status = "response_error"
                    job.error = "Amplify returned an unrecognized receipt. Check run history before retrying."
                    logger.error("Amplify job %s returned an invalid workflow receipt", job.id)
                else:
                    job.status = "accepted"
                    job.remote_run_id = str(receipt.run_id)
            else:
                job.status = "submission_failed"
                job.error = f"Amplify rejected the request (HTTP {response.status_code}). See response details."
                logger.warning("Amplify job %s rejected with HTTP %s", job.id, response.status_code)
    except httpx.RequestError as exc:
        job.status = "submission_unknown"
        job.error = "Connection interrupted; the remote run may have started. Check Amplify before creating another request."
        logger.warning("Amplify job %s transport failure: %s", job.id, type(exc).__name__)
    except (OSError, RuntimeError, ValueError, UnicodeError) as exc:
        job.status = "submission_unknown"
        job.error = "Submission could not be confirmed. Check Amplify run history and your token before another request."
        logger.error("Amplify job %s could not be confirmed: %s", job.id, type(exc).__name__)
    db.commit()
    db.refresh(job)
    return job
