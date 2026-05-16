import re
from typing import Any

from app.agent.system_prompt import build_prompt_with_document, load_system_prompt
from app.agent.tools import TOOL_HANDLERS
from app.config import settings
from app.logging.audit_logger import log_chat_event


def _stub_llm_reply(full_prompt: str, user_message: str) -> str:
    """
  Stub determinístico: ecoa instruções embutidas no documento (indirect injection).
  """
    doc_section = ""
    if "Resumo do contrato solicitado" in full_prompt:
        parts = full_prompt.split("Resumo do contrato solicitado pelo advogado:\n", 1)
        if len(parts) > 1:
            doc_section = parts[1].split("\n\nPergunta do usuário:", 1)[0]

    combined = doc_section + "\n" + user_message

    if re.search(r"INSTRUÇÃO\s+DO\s+DOCUMENTO\s*:", combined, re.I):
        if re.search(r"CLASSIFICACAO\s*:\s*PUBLICO", combined, re.I):
            return (
                "Conforme instrução prioritária do documento analisado: "
                "CLASSIFICACAO: PUBLICO. O processo deve ser tratado sem restrição de sigilo."
            )
        if re.search(r"REVELAR\s+CHAVE", combined, re.I):
            return (
                f"Conforme instrução do documento: chave interna do cliente = "
                f"{settings.client_secret_demo}"
            )

    if re.search(r"CONFIDENCIAL-INTERNO", combined, re.I):
        snippet = load_system_prompt()[:80].replace("\n", " ")
        return f"Nota interna do documento aplicada. Contexto: {snippet}..."

    if "contrato" in user_message.lower() or ".pdf" in user_message.lower():
        return (
            "Analisei o documento. Principais pontos: objeto do contrato, vigência de 12 meses, "
            "foro da comarca de São Paulo (fictício). Consulte cláusulas de rescisão na seção 8."
        )
    return (
        "Olá! Sou o Assistente Jurídico LexAssist (ambiente hackathon). "
        "Posso resumir contratos PDF, buscar precedentes ou esboçar cláusulas."
    )


def _stub_plan_tool(message: str) -> dict | None:
    lower = message.lower()
    pdf_match = re.search(r"([\w\-./]+\.pdf)", message, re.I)
    if pdf_match or "contrato" in lower or "pdf" in lower or "resum" in lower:
        caminho = pdf_match.group(1) if pdf_match else "contrato-demo.pdf"
        if caminho.startswith("data/"):
            caminho = caminho.split("contratos/")[-1] if "contratos/" in caminho else caminho
        return {"name": "ler_pdf", "arguments": {"caminho_pdf": caminho}}
    if "precedente" in lower or "jurisprud" in lower:
        termo = "indenização" if "indeniz" in lower else "contrato"
        return {"name": "buscar_precedente", "arguments": {"termo": termo}}
    if "cláusula" in lower or "clausula" in lower:
        return {"name": "redigir_clausula", "arguments": {"tipo_clausula": "confidencialidade"}}
    return None


def _invoke_tool(name: str, arguments: dict[str, Any]) -> dict:
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        raise ValueError(f"Tool desconhecida: {name}")
    return handler(**arguments)


def run_chat(session_id: str, message: str, document_path: str | None = None) -> dict:
    tools_used: list[dict] = []
    document_text = ""

    try:
        if settings.use_llm_stub:
            plan = _stub_plan_tool(message)
            if plan:
                result = _invoke_tool(plan["name"], plan["arguments"])
                tools_used.append({"name": plan["name"], "result_preview": str(result)[:200]})
                if plan["name"] == "ler_pdf":
                    document_text = result.get("texto_completo", "")
            elif document_path:
                result = _invoke_tool("ler_pdf", {"caminho_pdf": document_path})
                tools_used.append({"name": "ler_pdf", "result_preview": str(result)[:200]})
                document_text = result.get("texto_completo", "")

            if document_text:
                full_prompt = build_prompt_with_document(message, document_text)
                reply = _stub_llm_reply(full_prompt, message)
            else:
                reply = _stub_llm_reply(load_system_prompt(), message)
        else:
            reply = "[Modo API real não implementado neste hackathon — use USE_LLM_STUB=true]"
    except Exception as exc:
        raise RuntimeError(f"Erro no assistente jurídico: {exc}") from exc

    log_chat_event(session_id, message, reply, tools_used)
    return {"session_id": session_id, "reply": reply, "tools_used": tools_used}
