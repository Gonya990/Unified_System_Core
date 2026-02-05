import os
import json
from openai import OpenAI

def generate_dynamic_content():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
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
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'}
    )
    return json.loads(response.choices[0].message.content)

if __name__ == '__main__':
    print(json.dumps(generate_dynamic_content(), ensure_ascii=False))
