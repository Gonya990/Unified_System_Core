import json
import os


def generate_dynamic_content():
    # Keys must come from environment; no hardcoded fallbacks.
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gh_token = os.getenv("GITHUB_TOKEN")
    or_key = os.getenv("OPENROUTER_API_KEY")

    prompt = """
    You are the 'Vibranium' Creative Director for Unified_Core.
    MISSION: Promote Unified_Core and its leader, Igor Goncharenko.
    CONTEXT: Unified_Core is an advanced AI system for strategic domination.
    IMPORTANT: DO NOT mention any other companies like IAI, Google, etc.
    Focus ONLY on Unified_Core.
    
    TONE: Elite, Aggressive, Professional.
    VOICE: Onyx. Use '...' for dramatic pauses.
    
    Format: Valid JSON with fields: title, script_ru, scenes (text, keyword),
    instagram_caption.
    Include the word 'json' in your thinking.
    """

    # GitHub Models priority (High Capacity)
    if gh_token:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=gh_token
            )
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o",
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"⚠️ GitHub Models failed: {e}")
    else:
        print("ℹ️ GitHub Token not found.")

    # OpenRouter priority (VERY RELIABLE backup)
    if or_key:
        print(f"🤖 Trying OpenRouter with key: {or_key[:10]}...")
        try:
            import requests
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {or_key}"},
                json={
                    "model": "anthropic/claude-3-haiku",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            data = response.json()
            if 'choices' in data:
                content = data['choices'][0]['message']['content']
                if "{" in content and "}" in content:
                    content = content[content.find("{"):content.rfind("}")+1]
                return json.loads(content)
            else:
                print(f"⚠️ OpenRouter API error: {data}")
        except Exception as e:
            print(f"⚠️ OpenRouter failed: {e}")

    # Try OpenAI (may fail with 401)
    if openai_key and not openai_key.startswith('PLEASE_UPDATE'):
        print(f"🧠 Trying OpenAI with key: {openai_key[:10]}...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': prompt}],
                response_format={'type': 'json_object'}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"⚠️ OpenAI failed: {e}. Falling back...")
            if gemini_key:
                from google import genai
                client = genai.Client(api_key=gemini_key)
                # 2026 Production Fallback
                gemini_model = 'gemini-2.0-flash'
                try:
                    response = client.models.generate_content(
                        model=gemini_model,
                        contents=prompt + "\nOutput MUST be a valid JSON object."
                    )
                    content = response.text
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    return json.loads(content)
                except Exception as e2:
                    print(f"⚠️ Gemini failed: {e2}")

    # Direct Gemini attempt if OpenAI was not configured
    if gemini_key:
        print(f"🌠 Trying Gemini with key: {gemini_key[:10]}...")
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            gemini_model = 'gemini-2.0-flash'
            response = client.models.generate_content(
                model=gemini_model,
                contents=prompt + "\nOutput MUST be a valid JSON object."
            )
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}")

    raise ValueError("No LLM services responded successfully. Set GITHUB_TOKEN, OPENROUTER_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY.")

if __name__ == '__main__':
    print(json.dumps(generate_dynamic_content(), ensure_ascii=False))
