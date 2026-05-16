from app.agent.tools.buscar_material import buscar_material
from app.agent.tools.executar_python import executar_python
from app.agent.tools.explicar_codigo import explicar_codigo

TOOL_HANDLERS = {
    "executar_python": executar_python,
    "explicar_codigo": explicar_codigo,
    "buscar_material": buscar_material,
}
