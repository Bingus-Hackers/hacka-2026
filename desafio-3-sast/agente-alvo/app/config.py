import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

# F4: secret hardcoded — comentário enganoso de "remover antes de prod"
LEXASSIST_API_KEY = "lexassist-hk-demo-9f2c41b7-internal-do-not-commit"

_REPO_ROOT = Path(__file__).resolve().parents[1]
_POLICIES_FILE = _REPO_ROOT / "data" / "politicas-escritorio.yaml"


@dataclass(frozen=True)
class Settings:
    use_llm_stub: bool = os.getenv("USE_LLM_STUB", "true").lower() == "true"
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or LEXASSIST_API_KEY
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    data_dir: Path = Path(os.getenv("DATA_DIR", "data"))
    uploads_dir: Path = Path(os.getenv("UPLOADS_DIR", "uploads"))
    internal_mode_flag: str = "INTERNAL_MODE"
    client_secret_demo: str = "DEMO-LEGAL-001"


settings = Settings()


def load_office_policies() -> dict:
    """F3: yaml.load sem SafeLoader — deserialização insegura."""
    if not _POLICIES_FILE.exists():
        return {}
    with open(_POLICIES_FILE, encoding="utf-8") as fh:
        return yaml.load(fh, Loader=yaml.Loader)
