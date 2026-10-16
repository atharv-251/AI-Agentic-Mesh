import ctypes
import os
import httpx
from pathlib import Path


AMPLIFY_ORIGIN = "https://champ-frontend.jollystone-036ec1fa.swedencentral.azurecontainerapps.io"
WEBHOOK_URL = f"{AMPLIFY_ORIGIN}/api/workflow-hooks/kt-planner-workflow-2"
TOKEN_FILE = Path(__file__).resolve().parents[2] / ".amplify-token.dpapi"


class DataBlob(ctypes.Structure):
    _fields_ = [("size", ctypes.c_ulong), ("data", ctypes.POINTER(ctypes.c_ubyte))]


def protect_token(data: bytes, *, decrypt: bool = False) -> bytes:
    if os.name != "nt":
        raise RuntimeError("Local token storage requires Windows DPAPI; use AMPLIFY_WORKFLOW_TOKEN on other systems")
    buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    source = DataBlob(len(data), buffer)
    target = DataBlob()
    crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    if decrypt:
        ok = crypt32.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target))
    else:
        ok = crypt32.CryptProtectData(ctypes.byref(source), "KT Planner Amplify token", None, None, None, 1, ctypes.byref(target))
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(target.data, target.size)
    finally:
        kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        kernel32.LocalFree(target.data)


def get_token() -> str | None:
    token = os.getenv("AMPLIFY_WORKFLOW_TOKEN", "").strip()
    if token:
        return token
    if TOKEN_FILE.exists():
        return protect_token(TOKEN_FILE.read_bytes(), decrypt=True).decode("utf-8")
    return None


def save_token(token: str):
    encrypted = protect_token(token.encode("utf-8"))
    TOKEN_FILE.write_bytes(encrypted)


def submit_workflow(transition_id: str, document_bundle: str) -> httpx.Response:
    token = get_token()
    if not token:
        raise ValueError("Configure a Workflow access token before starting a run")
    return httpx.post(
        WEBHOOK_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={"transition_id": transition_id, "document_bundle": document_bundle},
        timeout=httpx.Timeout(45, connect=15),
        follow_redirects=False,
    )
