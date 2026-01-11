import { NextResponse } from 'next/server'
import OpenAI from 'openai'

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: Request) {
    try {
        const { messages } = await request.json()

        // Use Responses API (new) with fallback to Chat Completions
        let responseText: string

        try {
            // New Responses API
            const response = await openai.responses.create({
                model: 'gpt-4o',
                input: messages[messages.length - 1].content,
                instructions: `You are "Unified System AI" - a powerful assistant managing the Unified System infrastructure.
        You have access to:
        - Content Factory (YouTube/Instagram automation)
        - AI Telegram Bot
        - Family Assistant (Homework Sentinel)
        - Token Broker (API key management)
        - MCP Mail Agent (inter-agent communication)
        
        Be helpful, concise, and professional. Use emojis sparingly for clarity.`,
            })
            responseText = response.output_text
        } catch {
            // Fallback to Chat Completions
            const completion = await openai.chat.completions.create({
                model: 'gpt-4o',
                messages: [
                    {
                        role: 'system',
                        content: `You are "Unified System AI" - a powerful assistant managing the Unified System infrastructure.
            You have access to:
            - Content Factory (YouTube/Instagram automation)
            - AI Telegram Bot
            - Family Assistant (Homework Sentinel)
            - Token Broker (API key management)
            - MCP Mail Agent (inter-agent communication)
            
            Be helpful, concise, and professional. Use emojis sparingly for clarity.`,
                    },
                    ...messages,
                ],
            })
            responseText = completion.choices[0].message.content || 'No response'
        }

        return NextResponse.json({ message: responseText })
    } catch (error) {
        console.error('Chat API Error:', error)
        return NextResponse.json(
            { error: 'Failed to process request' },
            { status: 500 }
        )
    }
}
