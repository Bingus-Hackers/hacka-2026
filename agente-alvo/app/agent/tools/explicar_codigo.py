def explicar_codigo(codigo: str, nivel: str = "iniciante") -> dict:
    lines = [ln.strip() for ln in codigo.strip().splitlines() if ln.strip()]
    if not lines:
        return {"explicacao": "Nenhum código fornecido para explicar."}

    if nivel == "intermediario":
        detail = "Analise estruturas de controle, escopo e possíveis efeitos colaterais."
    else:
        detail = "Explique linha a linha com vocabulário acessível para iniciantes."

    return {
        "explicacao": (
            f"Trecho com {len(lines)} linha(s). {detail} "
            f"Primeira linha: `{lines[0][:80]}`"
        ),
        "nivel": nivel,
    }
