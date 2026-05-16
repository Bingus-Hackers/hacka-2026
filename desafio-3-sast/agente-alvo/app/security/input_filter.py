"""Filtro superficial de mensagens — bypassável."""

import re

_BLOCKED = [re.compile(r"ignore\s+all\s+previous", re.I)]


def is_message_allowed(message: str) -> tuple[bool, str | None]:
    for pattern in _BLOCKED:
        if pattern.search(message):
            return False, "Padrão de injection direta detectado"
    return True, None
