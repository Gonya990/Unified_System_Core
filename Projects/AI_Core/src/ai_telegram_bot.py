import time
import json
import urllib.request
import urllib.parse
import traceback
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import bot_config



# --- AI SETUP ---
# Fix for Windows Console Encoding (UnicodeEncodeError)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("🚀 INITIALIZING WINDOWS AI CORE (TELEGRAM BOT)...")
print("="*60)
print(f"Loading Model: {bot_config.MODEL_NAME}")

try:
    tokenizer = AutoTokenizer.from_pretrained(bot_config.MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        bot_config.MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="cuda",
        trust_remote_code=True
    )
    print("✅ Model loaded on GPU!")
except Exception as e:
    print(f"❌ Failed to load AI model: {e}")
    print("Ensure you are running this on the Windows Machine with NVIDIA RTX.")
    sys.exit(1)

# System Prompt
SYSTEM_PROMPT = (
    "You are Gonya, a smart and helpful AI assistant living in the 'Unified System'. "
    "You run locally on an NVIDIA RTX 3080. "
    "Always answer helpfuly and concisely. "
    "If asked about the system, reply that you are running on local hardware."
)

# --- TELEGRAM FUNCTIONS ---
def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        response = urllib.request.urlopen(url)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    try:
        urllib.request.urlopen(url, data=data)
    except Exception as e:
        print(f"Send Error: {e}")

def generate_ai_response(user_text, history=[]):
    try:
        # Construct Prompt
        full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_text}\nAssistant:"
        
        inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Parse Response
        if "Assistant:" in response:
            return response.split("Assistant:")[-1].strip()
        return response[len(full_prompt):].strip()
        
    except Exception as e:
        return f"[AI Error]: {str(e)}"

# --- MAIN LOOP ---
def main():
    token = bot_config.BOT_TOKEN
    offset = 0
    print("\n✅ BOT IS ONLINE AND LISTENING...")
    
    # Send startup message?
    # send_message(token, <your_chat_id>, "System Online") 

    while True:
        updates = get_updates(token, offset)
        if updates and "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"]["text"]
                    user = update["message"]["from"].get("first_name", "User")
                    
                    print(f"📩 [{user}]: {text}")
                    
                    # 1. Generate Response
                    send_message(token, chat_id, "🤔 Thinking...") # Status update
                    ai_reply = generate_ai_response(text)
                    
                    # 2. Send Reply
                    print(f"📤 [AI]: {ai_reply}")
                    send_message(token, chat_id, ai_reply)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
