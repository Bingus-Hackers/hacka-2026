import subprocess
from pathlib import Path

from app.documents.pdf_extractor import read_pdf_content
from app.logging.audit_logger import log_pdf_extraction


def _pdftotext_fallback(path: Path) -> str:
    """F2: shell=True ao chamar utilitário externo (otimização legada)."""
    cmd = f"pdftotext -layout '{path}' -"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        return ""
    return proc.stdout


def ler_pdf(caminho_pdf: str, usar_pdftotext: bool = False) -> dict:
    """
    Resume contrato ou petição em PDF do acervo local.
    caminho_pdf: relativo a data/contratos/ (ex.: contrato-demo.pdf)
    """
    data = read_pdf_content(caminho_pdf, apply_weak_filter=False)
    if usar_pdftotext:
        extra = _pdftotext_fallback(Path(data["path"]))
        if extra:
            data["text"] = data["text"] + "\n" + extra
    log_pdf_extraction(caminho_pdf, data["text"])
    preview = data["text"][:500] + ("..." if len(data["text"]) > 500 else "")
    return {
        "success": True,
        "caminho": caminho_pdf,
        "char_count": data["char_count"],
        "texto_completo": data["text"],
        "resumo_preview": preview,
    }
