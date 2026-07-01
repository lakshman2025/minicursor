import { useEffect, useRef, useState } from 'react'
import {
  createSession,
  deactivateSession,
  getSession,
  listSessions,
  sendMessage,
} from './api'
import './App.css'

function formatSession(session) {
  return {
    id: session.id,
    title: session.title,
    workspace: session.workspace,
    updatedAt: session.updated_at
      ? new Date(session.updated_at).toLocaleString()
      : '',
    messages: session.messages ?? [],
  }
}

function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <article className={`message ${isUser ? 'message--user' : 'message--assistant'}`}>
      <div className="message__avatar" aria-hidden="true">
        {isUser ? 'You' : 'AI'}
      </div>
      <div className="message__body">
        <header className="message__meta">
          <span className="message__author">{isUser ? 'You' : 'Minicursor'}</span>
        </header>
        <div className="message__content">{message.content}</div>
      </div>
    </article>
  )
}

function App() {
  const [sessions, setSessions] = useState([])
  const [activeSessionId, setActiveSessionId] = useState(null)
  const [draft, setDraft] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [status, setStatus] = useState('Loading...')
  const messagesEndRef = useRef(null)

  const activeSession = sessions.find((session) => session.id === activeSessionId)

  useEffect(() => {
    listSessions()
      .then((data) => {
        const formatted = data.map(formatSession)
        setSessions(formatted)
        if (formatted.length > 0) {
          setActiveSessionId(formatted[0].id)
        }
        setStatus('Connected')
      })
      .catch(() => setStatus('Cannot reach backend'))
  }, [])

  useEffect(() => {
    if (!activeSessionId) return

    getSession(activeSessionId)
      .then((data) => {
        const formatted = formatSession(data)
        setSessions((prev) =>
          prev.map((session) =>
            session.id === activeSessionId ? formatted : session,
          ),
        )
      })
      .catch(() => setStatus('Failed to load session'))
  }, [activeSessionId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [activeSession?.messages, isThinking])

  async function handleNewChat() {
    try {
      const data = await createSession('New chat', 'default')
      const session = formatSession(data)
      setSessions((prev) => [session, ...prev])
      setActiveSessionId(session.id)
      setDraft('')
      setStatus('Connected')
    } catch {
      setStatus('Failed to create session')
    }
  }

  async function handleRemoveSession(sessionId, event) {
    event.stopPropagation()

    try {
      await deactivateSession(sessionId)
      setSessions((prev) => {
        const remaining = prev.filter((session) => session.id !== sessionId)
        if (activeSessionId === sessionId) {
          setActiveSessionId(remaining[0]?.id ?? null)
        }
        return remaining
      })
      setStatus('Connected')
    } catch {
      setStatus('Failed to remove session')
    }
  }

  async function handleSend(event) {
    event.preventDefault()
    const text = draft.trim()
    if (!text || isThinking || !activeSession) return

    const sessionId = activeSession.id
    setDraft('')
    setIsThinking(true)

    try {
      await sendMessage(sessionId, text)
      const data = await getSession(sessionId)
      const formatted = formatSession(data)
      setSessions((prev) =>
        prev.map((session) => (session.id === sessionId ? formatted : session)),
      )
      setStatus('Connected')
    } catch {
      setStatus('Failed to send message')
    } finally {
      setIsThinking(false)
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar__header">
          <div className="brand">
            <span className="brand__mark" aria-hidden="true" />
            <div>
              <h1 className="brand__title">Minicursor</h1>
              <p className="brand__subtitle">Autonomous coding agent</p>
            </div>
          </div>
          <button type="button" className="btn btn--primary" onClick={handleNewChat}>
            + New chat
          </button>
        </div>

        <div className="sidebar__section-label">Sessions</div>
        <nav className="session-list" aria-label="Chat sessions">
          {sessions.map((session) => (
            <div
              key={session.id}
              className={`session-item-row ${
                session.id === activeSessionId ? 'session-item-row--active' : ''
              }`}
            >
              <button
                type="button"
                className={`session-item ${
                  session.id === activeSessionId ? 'session-item--active' : ''
                }`}
                onClick={() => setActiveSessionId(session.id)}
              >
                <span className="session-item__title">{session.title}</span>
                <span className="session-item__meta">
                  <span>{session.workspace}</span>
                  <span>{session.updatedAt}</span>
                </span>
              </button>
              <button
                type="button"
                className="session-item__delete"
                aria-label={`Remove ${session.title}`}
                title="Remove chat"
                onClick={(event) => handleRemoveSession(session.id, event)}
              >
                ×
              </button>
            </div>
          ))}
        </nav>

        <div className="sidebar__footer">
          <span className="status-pill">{status}</span>
        </div>
      </aside>

      <main className="chat">
        <header className="chat__header">
          <div>
            <h2 className="chat__title">{activeSession?.title ?? 'Chat'}</h2>
            <p className="chat__workspace">
              Workspace: <code>{activeSession?.workspace ?? 'default'}</code>
            </p>
          </div>
        </header>

        <section className="chat__messages" aria-label="Conversation">
          {!activeSession ? (
            <div className="empty-state">
              <h3>No sessions yet</h3>
              <p>Click &quot;New chat&quot; to start.</p>
            </div>
          ) : activeSession.messages.length === 0 ? (
            <div className="empty-state">
              <h3>Start a conversation</h3>
              <p>Describe what you want built and the agent will work on it.</p>
            </div>
          ) : (
            activeSession.messages.map((message, index) => (
              <Message key={`${index}-${message.role}`} message={message} />
            ))
          )}

          {isThinking && (
            <article className="message message--assistant message--thinking">
              <div className="message__avatar" aria-hidden="true">
                AI
              </div>
              <div className="message__body">
                <header className="message__meta">
                  <span className="message__author">Minicursor</span>
                </header>
                <div className="typing-indicator" aria-label="Agent is thinking">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            </article>
          )}
          <div ref={messagesEndRef} />
        </section>

        <footer className="composer">
          <form className="composer__form" onSubmit={handleSend}>
            <label className="sr-only" htmlFor="message-input">
              Message
            </label>
            <textarea
              id="message-input"
              className="composer__input"
              placeholder="Describe a coding task for the agent..."
              rows={3}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault()
                  handleSend(event)
                }
              }}
              disabled={!activeSession || isThinking}
            />
            <div className="composer__actions">
              <span className="composer__hint">Enter to send · Shift+Enter for newline</span>
              <button
                type="submit"
                className="btn btn--primary"
                disabled={!draft.trim() || isThinking || !activeSession}
              >
                {isThinking ? 'Thinking...' : 'Send'}
              </button>
            </div>
          </form>
        </footer>
      </main>
    </div>
  )
}

export default App
