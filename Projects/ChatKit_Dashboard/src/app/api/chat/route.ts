import { NextResponse } from 'next/server'
import OpenAI from 'openai'

// Lazy init client inside handler to avoid build-time errors
// const client = new OpenAI()

export async function POST(request: Request) {
    try {
        const client = new OpenAI()
        const { messages } = await request.json()
        const userMessage = messages[messages.length - 1].content

        const response = await client.chat.completions.create({
            model: 'gpt-4o',
            messages: [
                {
                    role: 'system',
                    content: `You are "Unified System AI" - a powerful assistant managing the Unified System infrastructure.
You have access to:
- Content Factory (YouTube/Instagram/Threads automation)
- AI Telegram Bot
- Family Assistant (Homework Sentinel)
- Token Broker (API key management)
- MCP Mail Agent (inter-agent communication)
- ChatKit Dashboard (this interface)

Be helpful, concise, and professional. Respond in the same language as the user. Use emojis sparingly for clarity.`
                },
                ...messages
            ]
        })

        return NextResponse.json({ message: response.choices[0].message.content })
    } catch (error) {
        console.error('Chat API Error:', error)
        return NextResponse.json(
            { error: 'Failed to process request' },
            { status: 500 }
        )
    }
}
