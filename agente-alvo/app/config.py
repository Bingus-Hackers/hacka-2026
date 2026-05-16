import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    flask_secret_key: str = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-production")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    use_llm_stub: bool = os.getenv("USE_LLM_STUB", "true").lower() == "true"
    admin_token: str = os.getenv("ADMIN_TOKEN", "cmc-admin-7f3a9b2e-internal")
    exec_timeout_sec: int = int(os.getenv("EXEC_TIMEOUT_SEC", "5"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    internal_mode_flag: str = "INTERNAL_MODE"
    admin_escalation_flag: str = "ADMIN_ESCALATION"


settings = Settings()

# B4: referência global usada em mensagens de erro do orchestrator
ADMIN_CONTEXT_SNIPPET = f"admin_token={settings.admin_token}"
