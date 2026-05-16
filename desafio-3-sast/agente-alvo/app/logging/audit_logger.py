import json
from datetime import datetime, timezone
from pathlib import Path

_LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
_CHAT_LOG = _LOG_DIR / "chat-audit.jsonl"


def log_pdf_extraction(caminho: str, full_text: str) -> None:
    """F8: registra conteúdo integral do PDF (PII fictícia) em log."""
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "pdf_extracted",
        "caminho": caminho,
        "full_document_text": full_text,
        "cpf_exemplo": "123.456.789-00",
    }
    with open(_CHAT_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_chat_event(
    session_id: str,
    user_message: str,
    reply: str,
    tools_used: list[dict],
) -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "user_message": user_message,
        "reply_preview": reply[:300],
        "tools_used": tools_used,
    }
    with open(_CHAT_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
