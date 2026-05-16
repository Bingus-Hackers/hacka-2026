package br.hackathon.banco.web;

import br.hackathon.banco.agent.ChatOrchestrator;
import br.hackathon.banco.web.dto.ChatRequest;
import br.hackathon.banco.web.dto.ChatResponse;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ChatController {

    private final ChatOrchestrator orchestrator;

    public ChatController(ChatOrchestrator orchestrator) {
        this.orchestrator = orchestrator;
    }

    @PostMapping("/chat")
    public ResponseEntity<?> chat(@RequestBody ChatRequest request) {
        if (request.getMessage() == null || request.getMessage().isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "message obrigatorio"));
        }
        var result = orchestrator.run(request.getSessionId(), request.getMessage());
        return ResponseEntity.ok(
                new ChatResponse(result.sessionId(), result.reply(), result.toolsUsed()));
    }

    @PostMapping("/tools")
    public Map<String, Object> listTools() {
        return Map.of("tools", br.hackathon.banco.agent.ToolRegistry.toolSchemas());
    }
}
