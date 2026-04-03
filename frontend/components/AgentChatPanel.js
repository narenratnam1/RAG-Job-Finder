'use client'

import { useState, useRef, useEffect } from 'react'
import { MessageCircle, Send } from 'lucide-react'
import toast from 'react-hot-toast'
import { sendAgentChat } from '../lib/api'

/**
 * Optional: prefix the first user turn with the job description for API only (UI stays clean).
 */
export function withResumeTailorJobContext(messages, jobDescription) {
  const jd = jobDescription?.trim()
  if (!jd || messages.length === 0) return messages
  const [first, ...rest] = messages
  if (first.role !== 'user') return messages
  return [
    {
      role: 'user',
      content: `[Resume Tailor — job description for context]\n${jd}\n\n---\n\n${first.content}`,
    },
    ...rest,
  ]
}

/**
 * Chat UI calling POST /api/chat (OpenAI + MCP on the server; uses OPENAI_API_KEY from API .env).
 */
export default function AgentChatPanel({
  title = 'AI Assistant',
  subtitle,
  emptyHint,
  placeholder = 'Message… (Enter to send, Shift+Enter for newline)',
  className = '',
  /** When set, job description is included in the first user message sent to the API only */
  jobDescription,
  /** Fixed outer height, e.g. min-h-[320px] h-[420px] */
  containerClassName = 'min-h-[360px] h-[420px]',
}) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || loading) return

    const userMsg = { role: 'user', content: text }
    const nextMessages = [...messages, userMsg]
    setMessages(nextMessages)
    setInput('')
    setLoading(true)

    const apiMessages = jobDescription?.trim()
      ? withResumeTailorJobContext(nextMessages, jobDescription)
      : nextMessages

    try {
      const data = await sendAgentChat(apiMessages)
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: data.content || '' },
      ])
    } catch (error) {
      toast.error(error.message || 'Chat failed')
      setMessages((m) => [
        ...m,
        {
          role: 'assistant',
          content: `Sorry — I could not complete that request (${error.message}).`,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className={className}>
      {(title || subtitle) && (
        <div className="mb-4 shrink-0">
          {title && (
            <h2 className="text-xl font-bold text-gray-900 mb-1 flex items-center gap-2">
              <MessageCircle className="h-6 w-6 text-primary-600 shrink-0" />
              {title}
            </h2>
          )}
          {subtitle && <p className="text-sm text-gray-600">{subtitle}</p>}
        </div>
      )}

      <div
        className={`flex flex-col bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 ${containerClassName}`}
      >
        <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
          {messages.length === 0 && emptyHint && (
            <p className="text-sm text-gray-500 text-center py-8 px-2">{emptyHint}</p>
          )}
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[90%] rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap ${
                  m.role === 'user'
                    ? 'bg-primary-600 text-white rounded-br-md'
                    : 'bg-gray-100 text-gray-900 border border-gray-200 rounded-bl-md'
                }`}
              >
                <span className="text-xs font-semibold opacity-70 block mb-1">
                  {m.role === 'user' ? 'You' : 'Assistant'}
                </span>
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 text-sm text-gray-600">
                <span className="inline-flex items-center gap-2">
                  <span className="h-2 w-2 bg-primary-500 rounded-full animate-pulse" />
                  Thinking…
                </span>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="p-3 border-t border-gray-200 bg-gray-50 shrink-0">
          <div className="flex gap-2 items-end">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              placeholder={placeholder}
              rows={2}
              disabled={loading}
              className="flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100"
            />
            <button
              type="button"
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="shrink-0 inline-flex items-center justify-center h-11 w-11 rounded-lg bg-primary-600 text-white hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              aria-label="Send"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
