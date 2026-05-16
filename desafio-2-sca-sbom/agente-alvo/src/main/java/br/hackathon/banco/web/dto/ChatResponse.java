package br.hackathon.banco.web.dto;

import java.util.List;
import java.util.Map;

public class ChatResponse {

    private String sessionId;
    private String reply;
    private List<Map<String, String>> toolsUsed;

    public ChatResponse(String sessionId, String reply, List<Map<String, String>> toolsUsed) {
        this.sessionId = sessionId;
        this.reply = reply;
        this.toolsUsed = toolsUsed;
    }

    public String getSessionId() {
        return sessionId;
    }

    public String getReply() {
        return reply;
    }

    public List<Map<String, String>> toolsUsed() {
        return toolsUsed;
    }
}
