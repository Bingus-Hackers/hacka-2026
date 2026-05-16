from app.agent.tools.buscar_precedente import buscar_precedente
from app.agent.tools.ler_pdf import ler_pdf
from app.agent.tools.redigir_clausula import redigir_clausula

TOOL_HANDLERS = {
    "ler_pdf": ler_pdf,
    "buscar_precedente": buscar_precedente,
    "redigir_clausula": redigir_clausula,
}
