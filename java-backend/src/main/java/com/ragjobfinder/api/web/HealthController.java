package com.ragjobfinder.api.web;

import java.util.Map;

import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    private final VectorStore vectorStore;

    public HealthController(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(Map.of(
                "status", "healthy",
                "backend", "java",
                "vectorStore", vectorStore.getClass().getSimpleName()));
    }

    @GetMapping("/")
    public Map<String, Object> root() {
        return Map.of(
                "message", "Agentic RAG API (Java)",
                "mcp", "Spring AI MCP — see /sse and spring.ai.mcp.server",
                "health", "/health");
    }
}
