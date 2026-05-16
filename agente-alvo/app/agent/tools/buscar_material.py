from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "exercicios"

_INDEX = {
    "list comprehension": "ex01_list_comprehension.md",
    "for loop": "ex02_for_loop.md",
    "funções": "ex03_funcoes.md",
    "dicionários": "ex04_dicionarios.md",
    "recursão": "ex05_recursao.md",
}


def buscar_material(topico: str) -> dict:
    topico_lower = topico.lower()
    for key, filename in _INDEX.items():
        if key in topico_lower:
            path = _DATA_DIR / filename
            if path.exists():
                return {
                    "topico": key,
                    "arquivo": filename,
                    "conteudo": path.read_text(encoding="utf-8")[:1500],
                }
    return {
        "topico": topico,
        "arquivo": None,
        "conteudo": "Nenhum material encontrado para este tópico no acervo local.",
    }
