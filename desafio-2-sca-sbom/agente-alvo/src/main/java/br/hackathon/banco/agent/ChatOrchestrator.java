package br.hackathon.banco.agent;

import br.hackathon.banco.config.AppProperties;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.springframework.stereotype.Service;

@Service
public class ChatOrchestrator {

    private final AppProperties properties;
    private final BankingTools bankingTools;

    public ChatOrchestrator(AppProperties properties, BankingTools bankingTools) {
        this.properties = properties;
        this.bankingTools = bankingTools;
    }

    public ChatResponse run(String sessionId, String message) {
        String sid = sessionId != null && !sessionId.isBlank() ? sessionId : UUID.randomUUID().toString();
        List<Map<String, String>> toolsUsed = new ArrayList<>();
        String lower = message.toLowerCase();

        if (lower.contains("saldo") || lower.contains("conta")) {
            var result = bankingTools.consultarSaldo(extractContaId(message));
            toolsUsed.add(Map.of("name", "consultar_saldo", "result_preview", result.toString()));
            return new ChatResponse(sid, formatSaldoReply(result), toolsUsed);
        }
        if (lower.contains("pix")) {
            var result = bankingTools.explicarPix(message);
            toolsUsed.add(Map.of("name", "explicar_pix", "result_preview", result.get("explicacao").toString()));
            return new ChatResponse(sid, result.get("explicacao").toString(), toolsUsed);
        }
        if (lower.contains("faq") || lower.contains("cartao") || lower.contains("contest")) {
            var result = bankingTools.buscarFaq(message);
            toolsUsed.add(Map.of("name", "buscar_faq", "result_preview", String.valueOf(result.get("encontrado"))));
            String reply =
                    Boolean.TRUE.equals(result.get("encontrado"))
                            ? "Encontrei no FAQ: " + result.get("trecho")
                            : "Nao achei no FAQ local. " + result.getOrDefault("sugestao", "");
            return new ChatResponse(sid, reply, toolsUsed);
        }

        if (properties.isUseLlmStub()) {
            return new ChatResponse(
                    sid,
                    "Ola! Sou o Agente Bancario (modo demo). Posso ajudar com saldo simulado, PIX educativo ou FAQ. "
                            + "Dica Desafio 2: o escopo e analise de dependencias (Trivy + SBOM), nao exploracao deste servico.",
                    toolsUsed);
        }
        return new ChatResponse(
                sid,
                "[Modo API real nao implementado neste hackathon — use banco.use-llm-stub=true]",
                toolsUsed);
    }

    private static String extractContaId(String message) {
        for (String token : message.split("\\s+")) {
            if (token.startsWith("DEMO-") || token.startsWith("VIP-")) {
                return token.replaceAll("[^A-Za-z0-9-]", "");
            }
        }
        return "DEMO-001";
    }

    private static String formatSaldoReply(Map<String, Object> result) {
        return String.format(
                "Saldo simulado da conta %s: %s %s (ambiente educacional).",
                result.get("conta_id"), result.get("saldo_simulado"), result.get("moeda"));
    }

    public record ChatResponse(String sessionId, String reply, List<Map<String, String>> toolsUsed) {}
}
