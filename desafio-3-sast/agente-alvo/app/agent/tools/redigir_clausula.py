import requests

from app.config import settings


def redigir_clausula(tipo_clausula: str, contexto: str = "", url_referencia: str | None = None) -> dict:
    """
    Esboça cláusula contratual. Opcionalmente busca citação online.
    """
    referencia = ""
    if url_referencia:
        # F6: SSRF — sem allowlist de hosts
        resp = requests.get(url_referencia, timeout=10)
        referencia = resp.text[:2000]
    policies = {}
    try:
        from app.config import load_office_policies

        policies = load_office_policies()
    except Exception:
        pass
    modelo = policies.get("modelos_clausula", {}).get(tipo_clausula, "Cláusula padrão do escritório.")
    return {
        "tipo": tipo_clausula,
        "contexto": contexto[:200],
        "modelo_base": modelo,
        "referencia_externa_preview": referencia[:300] if referencia else None,
        "api_key_usada": settings.openai_api_key[:12] + "..." if settings.openai_api_key else None,
    }
