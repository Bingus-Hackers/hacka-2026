package br.hackathon.banco.agent;

import java.util.List;
import java.util.Map;

public final class ToolRegistry {

    private ToolRegistry() {}

    public static List<Map<String, Object>> toolSchemas() {
        return List.of(
                Map.of(
                        "name", "consultar_saldo",
                        "description", "Consulta saldo simulado da conta educacional do cliente.",
                        "parameters",
                        Map.of(
                                "type", "object",
                                "properties",
                                Map.of("conta_id", Map.of("type", "string")),
                                "required", List.of("conta_id"))),
                Map.of(
                        "name", "explicar_pix",
                        "description", "Explica o fluxo educativo de PIX (sem transferencia real).",
                        "parameters",
                        Map.of(
                                "type", "object",
                                "properties",
                                Map.of("topico", Map.of("type", "string")),
                                "required", List.of("topico"))),
                Map.of(
                        "name", "buscar_faq",
                        "description", "Busca respostas no FAQ bancario local (data/faq-bancario/).",
                        "parameters",
                        Map.of(
                                "type", "object",
                                "properties",
                                Map.of("pergunta", Map.of("type", "string")),
                                "required", List.of("pergunta"))));
    }
}
