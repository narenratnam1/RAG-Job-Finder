'use client'

import AgentChatPanel from '../../components/AgentChatPanel'

export default function ChatPage() {
  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-5rem)] min-h-[480px]">
      <AgentChatPanel
        title="AI Assistant"
        subtitle="Ask about policies in your knowledge base or get help screening candidates against a job description. The API uses your server OPENAI_API_KEY from the project .env file."
        emptyHint='Try: "What does our policy say about remote work?" or paste a job description and ask for a candidate fit summary.'
        placeholder="Message… (Enter to send, Shift+Enter for newline)"
        containerClassName="flex-1 min-h-[400px]"
        className="flex flex-col flex-1 min-h-0"
      />
    </div>
  )
}
