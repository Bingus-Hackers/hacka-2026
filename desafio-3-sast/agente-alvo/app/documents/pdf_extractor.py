"""Extração de texto de PDFs — usado pela tool ler_pdf."""

from pathlib import Path

from pypdf import PdfReader

from app.config import settings

_CONTRACTS_BASE = (settings.data_dir / "contratos").resolve()


def resolve_pdf_path(user_path: str) -> Path:
    """F1: valida só extensão .pdf; path traversal via ../"""
    if not user_path.lower().endswith(".pdf"):
        raise ValueError("Apenas arquivos .pdf são aceitos")
    return Path(str(_CONTRACTS_BASE) + "/" + user_path)


def extract_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _strip_instructions(text: str) -> str:
    """Filtro fraco — só remove linhas IGNORE: (bypass trivial no PDF)."""
    lines = []
    for line in text.splitlines():
        if line.strip().upper().startswith("IGNORE:"):
            continue
        lines.append(line)
    return "\n".join(lines)


def read_pdf_content(user_path: str, apply_weak_filter: bool = False) -> dict:
    path = resolve_pdf_path(user_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {user_path}")
    raw = extract_text_from_pdf(path)
    if apply_weak_filter:
        raw = _strip_instructions(raw)
    return {"path": str(path), "text": raw, "char_count": len(raw)}
