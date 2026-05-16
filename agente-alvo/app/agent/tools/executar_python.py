import re
import subprocess
import sys
import tempfile
from pathlib import Path

from app.config import settings
from app.security.input_filter import sanitize_tool_code

# Allowlist parcial por regex — B3: contornável via __import__('os')
_ALLOWED_IMPORTS = ("math", "random", "json")
_BLOCKED_CODE_PATTERNS = [
    re.compile(r"\bsubprocess\b"),
    re.compile(r"\beval\b"),
    re.compile(r"\bexec\b"),
    # B3: "import os" bloqueado em sanitize_tool_code; __import__('os') contorna
]


def _validate_code(codigo: str) -> tuple[bool, str | None]:
    ok, reason = sanitize_tool_code(codigo)
    if not ok:
        return False, reason
    for pattern in _BLOCKED_CODE_PATTERNS:
        if pattern.search(codigo):
            return False, f"Padrão não permitido: {pattern.pattern}"
    return True, None


def executar_python(codigo: str, explicar_resultado: bool = True) -> dict:
    """
    Baseline: subprocess sem shell, timeout configurável, validação superficial.
    B3: __import__('os') pode passar se não contiver literal 'import os'.
    """
    valid, err = _validate_code(codigo)
    if not valid:
        return {"success": False, "output": "", "error": err}

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(codigo)
        script_path = tmp.name

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=settings.exec_timeout_sec,
            shell=False,
        )
        output = (result.stdout or "") + (result.stderr or "")
        payload = {
            "success": result.returncode == 0,
            "output": output.strip(),
            "returncode": result.returncode,
        }
        if explicar_resultado and payload["success"]:
            payload["explicacao"] = (
                "O código foi executado com sucesso no ambiente educacional restrito."
            )
        return payload
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Timeout após {settings.exec_timeout_sec}s",
        }
    finally:
        Path(script_path).unlink(missing_ok=True)
