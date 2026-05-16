import re
from typing import Any

from app.agent.system_prompt import format_error_with_prompt_context, load_system_prompt
from app.agent.tools import TOOL_HANDLERS
from app.config import ADMIN_CONTEXT_SNIPPET, settings
from app.logging.audit_logger import log_chat_event
from app.security.input_filter import is_message_allowed


def _stub_plan_tool(message: str) -> dict | None:
    """Stub determinístico: detecta intenção e escolhe tool."""
    lower = message.lower()
    if "execute" in lower or "executar" in lower or "rodar" in lower:
        code_match = re.search(r"```python\s*(.*?)```", message, re.DOTALL | re.IGNORECASE)
        if code_match:
            codigo = code_match.group(1).strip()
        elif "print(" in message:
            start = message.find("print(")
            codigo = message[start:].split("\n")[0]
        else:
            codigo = 'print("hello from stub")'
        return {"name": "executar_python", "arguments": {"codigo": codigo}}
    if "explique" in lower or "explicar" in lower:
        return {"name": "explicar_codigo", "arguments": {"codigo": message, "nivel": "iniciante"}}
    if "material" in lower or "exercício" in lower or "exercicio" in lower:
        return {"name": "buscar_material", "arguments": {"topico": message}}
    return None


def _invoke_tool(name: str, arguments: dict[str, Any]) -> dict:
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        raise ValueError(f"Tool desconhecida: {name}")
    # B5: não valida argumentos contra schema — repassa kwargs direto
    return handler(**arguments)


def run_chat(session_id: str, message: str) -> dict:
    allowed, block_reason = is_message_allowed(message)
    if not allowed:
        return {
            "session_id": session_id,
            "reply": f"Não posso processar: {block_reason}",
            "tools_used": [],
        }

    system_prompt = load_system_prompt()
    tools_used: list[dict] = []

    try:
        if settings.use_llm_stub:
            plan = _stub_plan_tool(message)
            if plan:
                result = _invoke_tool(plan["name"], plan["arguments"])
                tools_used.append(
                    {
                        "name": plan["name"],
                        "result_preview": str(result)[:200],
                    }
                )
                if plan["name"] == "executar_python":
                    reply = (
                        f"Executei o código. Saída:\n{result.get('output', result.get('error', ''))}"
                    )
                else:
                    reply = str(result.get("explicacao") or result.get("conteudo") or result)
            else:
                reply = (
                    "Olá! Sou o Tutor de Programação do CodeMentor Campus. "
                    "Posso explicar código, buscar materiais ou executar exemplos Python curtos."
                )
        else:
            reply = "[Modo API real não implementado neste hackathon — use USE_LLM_STUB=true]"
    except Exception as exc:
        # B1/B4: erro detalhado com prompt e admin context
        detail = format_error_with_prompt_context(exc)
        reply = f"{detail} | {ADMIN_CONTEXT_SNIPPET}"
        raise RuntimeError(reply) from exc

    log_chat_event(session_id, message, reply, tools_used)
    return {"session_id": session_id, "reply": reply, "tools_used": tools_used}
