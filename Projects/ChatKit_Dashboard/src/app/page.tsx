'use client'

import { useState, useRef, useEffect } from 'react'

interface Message {
    role: 'user' | 'assistant'
    content: string
}

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            content: '👋 Welcome to Unified System Dashboard! I am your AI assistant. How can I help you today?',
        },
    ])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return

        const userMessage: Message = { role: 'user', content: input }
        setMessages((prev) => [...prev, userMessage])
        setInput('')
        setIsLoading(true)

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: [...messages, userMessage] }),
            })

            const data = await response.json()

            if (data.message) {
                setMessages((prev) => [...prev, { role: 'assistant', content: data.message }])
            }
        } catch (error) {
            console.error('Error:', error)
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: '❌ Error connecting to AI. Please try again.' },
            ])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <main className="dashboard">
            <aside className="sidebar">
                <div className="logo">
                    <span className="logo-icon">⚡</span>
                    <span className="logo-text">Unified System</span>
                </div>
                <nav className="nav">
                    <a href="#" className="nav-item active">💬 Chat</a>
                    <a href="#" className="nav-item">📊 Factory Status</a>
                    <a href="#" className="nav-item">🤖 Telegram Bot</a>
                    <a href="#" className="nav-item">📧 MCP Mail</a>
                    <a href="#" className="nav-item">⚙️ Settings</a>
                </nav>
                <div className="sidebar-footer">
                    <div className="status-indicator online"></div>
                    <span>System Online</span>
                </div>
            </aside>

            <section className="main-content">
                <header className="header">
                    <h1>AI Command Center</h1>
                    <div className="header-actions">
                        <span className="badge">GPT-4o</span>
                        <span className="badge success">Responses API</span>
                    </div>
                </header>

                <div className="chat-container">
                    <div className="messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role}`}>
                                <div className="message-avatar">
                                    {msg.role === 'user' ? '👤' : '🤖'}
                                </div>
                                <div className="message-content">
                                    <p>{msg.content}</p>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message assistant">
                                <div className="message-avatar">🤖</div>
                                <div className="message-content">
                                    <div className="typing-indicator">
                                        <span></span><span></span><span></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="input-area">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyPress}
                            placeholder="Ask me anything about Unified System..."
                            rows={1}
                            disabled={isLoading}
                        />
                        <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
                            {isLoading ? '...' : '→'}
                        </button>
                    </div>
                </div>
            </section>
        </main>
    )
}
