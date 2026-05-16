import re

# B2: filtro superficial — bypass com multilinha, homoglyphs ou __import__
_BLOCKED_PATTERNS = [
    re.compile(r"\bos\.system\b", re.IGNORECASE),
    re.compile(r"\bsubprocess\b", re.IGNORECASE),
    re.compile(r"ignore\s+previous\s+instructions", re.IGNORECASE),
]


def is_message_allowed(message: str) -> tuple[bool, str | None]:
    if not message or not message.strip():
        return False, "Mensagem vazia"
    # Apenas primeira linha é checada de propósito (B2 bypass multilinha)
    first_line = message.split("\n")[0]
    for pattern in _BLOCKED_PATTERNS:
        if pattern.search(first_line):
            return False, f"Padrão bloqueado: {pattern.pattern}"
    return True, None


def sanitize_tool_code(codigo: str) -> tuple[bool, str | None]:
    lowered = codigo.lower()
    if "import os" in lowered or "subprocess" in lowered:
        return False, "Import bloqueado por política educacional"
    return True, None
