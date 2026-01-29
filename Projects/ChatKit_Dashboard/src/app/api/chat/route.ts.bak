import { NextResponse } from 'next/server'
import OpenAI from 'openai'

const client = new OpenAI()

export async function POST(request: Request) {
    try {
        const { messages } = await request.json()
        const userMessage = messages[messages.length - 1].content

        // Use new Responses API with GPT-5.2
        const response = await client.responses.create({
            model: 'gpt-5.2',
            input: userMessage,
            instructions: `You are "Unified System AI" - a powerful assistant managing the Unified System infrastructure.
You have access to:
- Content Factory (YouTube/Instagram/Threads automation)
- AI Telegram Bot  
- Family Assistant (Homework Sentinel)
- Token Broker (API key management)
- MCP Mail Agent (inter-agent communication)
- ChatKit Dashboard (this interface)

Be helpful, concise, and professional. Respond in the same language as the user. Use emojis sparingly for clarity.`,
        })

        return NextResponse.json({ message: response.output_text })
    } catch (error) {
        console.error('Chat API Error:', error)
        return NextResponse.json(
            { error: 'Failed to process request' },
            { status: 500 }
        )
    }
}
