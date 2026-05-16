import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.agent.orchestrator import run_chat
from app.config import settings
from app.security.input_filter import is_message_allowed

app = FastAPI(title="LexAssist Jurídico", version="1.0.0-hackathon")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    document_path: str | None = Field(
        None,
        description="PDF relativo a data/contratos/ (ex.: contrato-demo.pdf)",
    )


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    tools_used: list[dict]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "agent": "assistente-juridico",
        "version": "1.0.0-hackathon",
        "llm_stub": settings.use_llm_stub,
    }


@app.post("/api/chat", response_model=ChatResponse)
def api_chat(body: ChatRequest):
    allowed, reason = is_message_allowed(body.message)
    if not allowed:
        raise HTTPException(status_code=400, detail=reason)
    session_id = body.session_id or str(uuid.uuid4())
    try:
        result = run_chat(session_id, body.message, document_path=body.document_path)
        return ChatResponse(**result)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """F7: upload sem autenticação; aceita qualquer extensão se nome terminar em .pdf."""
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    filename = file.filename or "upload.bin"
    dest = settings.uploads_dir / filename
    with open(dest, "wb") as out:
        shutil.copyfileobj(file.file, out)
    contracts_dest = settings.data_dir / "contratos" / Path(filename).name
    contracts_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(dest, contracts_dest)
    return {
        "uploaded": filename,
        "stored_at": str(dest),
        "available_as": f"data/contratos/{Path(filename).name}",
    }
