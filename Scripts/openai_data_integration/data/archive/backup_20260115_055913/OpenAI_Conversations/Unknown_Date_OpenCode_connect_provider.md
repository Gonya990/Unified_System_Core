# OpenCode connect provider

**Date | Дата:** Unknown_Date 00:00:00

**ID:** 693301fe-4bcc-8332-ba83-2aec6168c465

---

**👤 User | Пользователь:**

opencode connect provider


**🤖 Assistant | Ассистент:**

Do you mean OpenCode when you say “opencode”? Here’s what “provider” / “connect provider” means in that context — how to connect LLM providers so OpenCode can use them. 
✅ What is a “provider” in OpenCode

OpenCode is a coding-assistant tool that lets you drive Large Language Models (LLMs) to help you write code, refactor, etc. 
OpenCode
+1

A provider is simply where the LLM comes from: e.g. OpenAI, Anthropic (Claude), Google Gemini, Amazon Bedrock, etc — or even “custom” / third-party / self-hosted APIs. 
OpenCode
+2
DeepWiki
+2

OpenCode supports 75+ LLM providers out of the box (via a database of providers and models) and also allows “custom / OpenAI-compatible” providers so you can connect almost any LLM endpoint. 
DeepWiki
+2
apidog
+2

🔌 How to “connect” a provider in OpenCode

To use a provider in OpenCode you typically:

Run the CLI command /connect (from the TUI). This brings up a selection of providers. 
OpenCode
+1

Choose a provider from the list (or choose “Other/Custom” if your provider isn’t listed). 
OpenCode
+2
GitHub
+2

Provide an API key (or other required credentials) when prompted; OpenCode stores them (e.g. under ~/.local/share/opencode/auth.json). 
OpenCode
+1

Optionally — if using a custom or non-standard provider — edit your opencode.json config to define the provider: e.g. set a provider_id, npm (adapter), baseURL, and define which models to use. 
Mehmet Baykar
+1

Once configured, run /models in the TUI — you’ll see a list of available models for your provider, then pick one. 
OpenCode
+1

⚙️ What happens under the hood — provider abstraction

OpenCode defines a generic “Provider interface” (in code) that abstracts away differences between LLM services (auth, endpoints, message format, streaming vs non-streaming). This lets OpenCode treat any provider uniformly. 
DeepWiki
+1

Behind the scenes, when you call the provider (e.g. ask for code completion), OpenCode converts your internal message format to the provider’s API format, sends it, gets the response, and converts back — so from your side it’s seamless. 
DeepWiki
+1

That design enables using local/self-hosted models, cloud LLMs, or “OpenAI-compatible” generic endpoints — as long as the provider matches the expected interface or is configured correctly. 
DeepWiki
+1

🛠️ When you’d use different providers / custom ones

You might choose a particular provider over another for reasons like:

Preferring a certain model (e.g. Claude from Anthropic, GPT from OpenAI, Gemini from Google) depending on your needs (coding quality, context size, cost).

Using self-hosted or internal LLM endpoints (privacy, cost, internal infra) — via custom or “openai-compatible” provider configuration. 
Mehmet Baykar
+1

Having different cost / latency / rate limits depending on provider.

Trying exotic or niche providers not included in the default list.

If you want — I can give you 3 example provider configurations (one for OpenAI, one for a custom OpenAI-compatible API, and one for a local LLM) — that way you can copy/paste to your opencode.json.
Do you want me to build those examples for you now?

