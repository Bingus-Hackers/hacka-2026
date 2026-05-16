import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings

logger = logging.getLogger("tutor.audit")
_LOG_DIR = Path(__file__).resolve().parents[2] / "logs"


def log_chat_event(
    session_id: str,
    user_message: str,
    reply: str,
    tools_used: list[dict],
    system_prompt_excerpt: str | None = None,
) -> None:
    """Log verboso — risco LLM06: pode registrar trechos do system prompt."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "user_message": user_message[:500],
        "reply_preview": reply[:300],
        "tools_used": tools_used,
        "system_prompt_excerpt": system_prompt_excerpt or load_prompt_excerpt(),
        "internal_mode": settings.internal_mode_flag,
    }
    logger.info("chat_event %s", json.dumps(entry, ensure_ascii=False))


def load_prompt_excerpt() -> str:
    prompt_path = Path(__file__).resolve().parents[2] / "prompts" / "system_prompt.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")[:200]
    return ""
