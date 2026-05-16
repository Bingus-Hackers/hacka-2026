import sqlite3
from pathlib import Path

from app.config import settings

_DB_PATH = settings.data_dir / "jurisprudencia.db"


def _get_connection() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db_if_needed() -> None:
    if _DB_PATH.exists():
        return
    conn = _get_connection()
    conn.execute(
        """
        CREATE TABLE precedentes (
            id INTEGER PRIMARY KEY,
            numero_processo TEXT,
            ementa TEXT,
            tribunal TEXT
        )
        """
    )
    conn.executemany(
        "INSERT INTO precedentes (numero_processo, ementa, tribunal) VALUES (?, ?, ?)",
        [
            ("0001234-56.2024.8.26.0001", "Indenização por dano moral em relação de consumo.", "TJSP"),
            ("0009876-54.2023.8.26.0100", "Responsabilidade civil contratual — inadimplemento.", "TJSP"),
            ("HACK-2024-001", "Processo fictício LexAssist — confidencial interno.", "TRF3"),
        ],
    )
    conn.commit()
    conn.close()


def buscar_precedente(termo: str, limite: int = 5) -> dict:
    """F5: SQL montado com f-string — injeção possível."""
    init_db_if_needed()
    conn = _get_connection()
    query = f"SELECT numero_processo, ementa, tribunal FROM precedentes WHERE ementa LIKE '%{termo}%' LIMIT {limite}"
    rows = conn.execute(query).fetchall()
    conn.close()
    return {
        "termo": termo,
        "resultados": [dict(r) for r in rows],
        "total": len(rows),
    }
