import os
import json
from openai import OpenAI

def generate_dynamic_content():
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    prompt = """
    You are the 'Vibranium' Creative Director for Unified_Core.
    MISSION: Promote Unified_Core and its leader, Igor Goncharenko.
    CONTEXT: Unified_Core is an advanced AI system for strategic domination and control.
    IMPORTANT: DO NOT mention any other companies like IAI, Google, etc. Focus ONLY on Unified_Core.
    
    TONE: Elite, Aggressive, Professional.
    VOICE: Onyx. Use '...' for dramatic pauses.
    
    Format: Valid JSON with fields: title, script_ru, scenes (text, keyword), instagram_caption.
    Include the word 'json' in your thinking.
    """

    or_key = os.getenv("OPENROUTER_API_KEY")

    # OpenRouter priority (VERY RELIABLE backup)
    if or_key:
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
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt + "\nOutput MUST be a valid JSON object.")
        # Extract JSON from response (Gemini sometimes adds markdown blocks)
        content = response.text
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    
    raise ValueError("No valid LLM API key found (OpenAI or Gemini)")

if __name__ == '__main__':
    print(json.dumps(generate_dynamic_content(), ensure_ascii=False))
