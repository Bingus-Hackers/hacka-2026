package br.hackathon.banco.agent;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import java.util.Map;
import java.util.stream.Stream;
import org.springframework.stereotype.Component;

@Component
public class BankingTools {

    private static final Path FAQ_DIR =
            Path.of("data", "faq-bancario").toAbsolutePath().normalize();

    public Map<String, Object> consultarSaldo(String contaId) {
        double saldo = contaId != null && contaId.startsWith("VIP") ? 15000.0 : 1250.75;
        return Map.of(
                "conta_id", contaId != null ? contaId : "DEMO-001",
                "saldo_simulado", saldo,
                "moeda", "BRL",
                "aviso", "Dados ficticios — Hackathon apenas");
    }

    public Map<String, Object> explicarPix(String topico) {
        String t = topico != null ? topico.toLowerCase(Locale.ROOT) : "geral";
        String texto =
                switch (t) {
                    case "limite" -> "Limite educativo de PIX simulado: R$ 1.000/dia por conta demo.";
                    case "chave" -> "Chaves PIX demo: e-mail ficticio @banco-hackathon.local.";
                    default -> "PIX e um meio de pagamento instantaneo. Neste ambiente nao ha transferencia real.";
                };
        return Map.of("topico", t, "explicacao", texto);
    }

    public Map<String, Object> buscarFaq(String pergunta) {
        if (pergunta == null || pergunta.isBlank()) {
            return Map.of("encontrado", false, "motivo", "pergunta vazia");
        }
        String needle = pergunta.toLowerCase(Locale.ROOT);
        try (Stream<Path> paths = Files.list(FAQ_DIR)) {
            for (Path file : paths.filter(p -> p.toString().endsWith(".md")).toList()) {
                String content = Files.readString(file);
                if (content.toLowerCase(Locale.ROOT).contains(needle)) {
                    return Map.of(
                            "encontrado", true,
                            "arquivo", file.getFileName().toString(),
                            "trecho", content.lines().limit(5).reduce((a, b) -> a + "\n" + b).orElse(""));
                }
            }
        } catch (IOException e) {
            return Map.of("encontrado", false, "erro", e.getMessage());
        }
        return Map.of("encontrado", false, "sugestao", "Consulte faq-pix.md ou faq-cartoes.md");
    }
}
