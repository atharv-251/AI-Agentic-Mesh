import logging
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, SecretStr

from backend.services import amplify_service


logger = logging.getLogger("kt_planner.amplify")
router = APIRouter(prefix="/api/v1/amplify", tags=["Amplify connection"])


def require_local_request(request: Request):
    if request.client is None or request.client.host not in ("127.0.0.1", "::1", "testclient"):
        raise HTTPException(status_code=403, detail="Amplify connection setup is available only on the local machine")
    origin = request.headers.get("origin")
    if origin and origin not in ("http://127.0.0.1:8000", "http://localhost:8000", "http://localhost:5173", "http://127.0.0.1:5173"):
        raise HTTPException(status_code=403, detail="Untrusted origin for local Amplify connection")
    if urlparse(str(request.base_url)).hostname not in ("127.0.0.1", "localhost", "::1", "testserver"):
        raise HTTPException(status_code=403, detail="Untrusted host for local Amplify connection")


class TokenSetup(BaseModel):
    token: SecretStr


@router.get("/connection")
def connection(request: Request):
    require_local_request(request)
    try:
        configured = bool(amplify_service.get_token())
    except (OSError, RuntimeError, UnicodeError) as exc:
        logger.error("Could not unlock local Amplify credentials: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Local Amplify credential cannot be unlocked; configure it again") from exc
    return {
        "configured": configured,
        "workflow_id": 167,
        "project_id": 77,
        "webhook_url": amplify_service.WEBHOOK_URL,
        "credential_storage": "Backend environment or Windows user-encrypted local file",
        "automatic_result_sync": False,
    }


@router.put("/connection")
def configure_connection(payload: TokenSetup, request: Request):
    require_local_request(request)
    value = payload.token.get_secret_value().strip()
    if not 20 <= len(value) <= 4096 or any(character.isspace() for character in value):
        raise HTTPException(status_code=422, detail="Paste the complete Workflow access token without whitespace")
    try:
        amplify_service.save_token(value)
    except (OSError, RuntimeError) as exc:
        logger.error("Could not persist Amplify credentials: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Could not store the token using Windows user encryption") from exc
    return {"configured": True, "message": "Token saved securely; execution has not yet been verified"}
