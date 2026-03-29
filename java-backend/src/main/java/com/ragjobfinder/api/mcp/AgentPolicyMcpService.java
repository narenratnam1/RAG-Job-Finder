package com.ragjobfinder.api.mcp;

import java.util.List;
import java.util.Map;

import org.springframework.ai.document.Document;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

/**
 * MCP tools mirroring the Python FastMCP "AgentPolicy" server (consult, screen, instructions).
 */
@SuppressWarnings("unchecked")
@Service
public class AgentPolicyMcpService {

    private final VectorStore vectorStore;

    public AgentPolicyMcpService(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @Tool(
            name = "consult_policy_db",
            description = "Consult the policy database using semantic search")
    public String consultPolicyDb(String query) {
        try {
            List<Document> docs = vectorStore.similaritySearch(
                    SearchRequest.builder().query(query).topK(3).build());
            if (docs.isEmpty()) {
                return "No relevant policy information found.";
            }
            StringBuilder sb = new StringBuilder();
            sb.append("Found ").append(docs.size()).append(" relevant policy documents:\n\n");
            int i = 1;
            for (Document doc : docs) {
                Map<String, Object> meta = doc.getMetadata();
                Object source = meta.getOrDefault("source", "Unknown");
                Object page = meta.getOrDefault("page", "N/A");
                sb.append("--- Result ").append(i).append(" ---\n");
                sb.append("Source: ").append(source).append("\n");
                sb.append("Page: ").append(page).append("\n");
                sb.append("Relevance Score: ").append(formatRelevance(doc)).append("\n");
                sb.append("Content:\n").append(doc.getText() != null ? doc.getText() : "").append("\n\n");
                i++;
            }
            return sb.toString();
        } catch (Exception e) {
            return "Error querying policy database: " + e.getMessage();
        }
    }

    @Tool(
            name = "screen_candidate",
            description = "Screen a candidate by comparing their resume against a job description")
    public String screenCandidate(String jobDescription) {
        try {
            List<Document> docs = vectorStore.similaritySearch(
                    SearchRequest.builder().query(jobDescription).topK(10).build());
            if (docs.isEmpty()) {
                return "No resume information found in the database. Please upload a resume first.";
            }
            StringBuilder contextParts = new StringBuilder();
            int i = 1;
            for (Document doc : docs) {
                Map<String, Object> meta = doc.getMetadata();
                Object page = meta.getOrDefault("page", "N/A");
                contextParts.append("[Part ").append(i).append(" - Page ").append(page).append("]:\n");
                contextParts.append(doc.getText() != null ? doc.getText() : "").append("\n\n");
                i++;
            }
            return """
                    CONTEXT: Here are the relevant parts of the candidate's resume:

                    %s

                    TASK: Compare the resume parts above against this Job Description:

                    %s"""
                    .formatted(contextParts.toString().trim(), jobDescription);
        } catch (Exception e) {
            return "Error screening candidate: " + e.getMessage();
        }
    }

    @Tool(
            name = "get_screener_instructions",
            description = "Get instructions for using the candidate screening tool")
    public String getScreenerInstructions() {
        return "1. Upload a PDF Resume. 2. In the chat, paste the Job Description and ask: \"Evaluate this candidate for this role.\" ";
    }

    /** Match Python formatting: relevance ≈ 1 - distance, or use vector similarity score when present. */
    private static String formatRelevance(Document doc) {
        Map<String, Object> meta = doc.getMetadata();
        Object d = meta.get("distance");
        if (d instanceof Number n) {
            return String.format("%.4f", 1.0 - n.doubleValue());
        }
        if (doc.getScore() != null) {
            return String.format("%.4f", doc.getScore());
        }
        return "n/a";
    }
}
