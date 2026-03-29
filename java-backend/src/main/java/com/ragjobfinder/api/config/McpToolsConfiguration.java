package com.ragjobfinder.api.config;

import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.ragjobfinder.api.mcp.AgentPolicyMcpService;

@Configuration
public class McpToolsConfiguration {

    @Bean
    public ToolCallbackProvider agentPolicyTools(AgentPolicyMcpService agentPolicyMcpService) {
        return MethodToolCallbackProvider.builder().toolObjects(agentPolicyMcpService).build();
    }
}
