from google import genai
from google.genai.types import GenerateContentConfig

GEMINI_API_KEY = "AIzaSyCZd986TK8vI-lk7ygpwMV0XgquWIHX7ZU"

def ask_gemini_3_for_ha_improvements():
    print("🧠 Asking Gemini 3 for Smart Home Architecture Improvements...")

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Context about current HA integration
    context = """
    Current Home Assistant (HA) integration in our AI Telegram Bot:
    - Dedicated 'HAController' class with fuzzy matching for lights/switches.
    - Supports: turn_on_light, turn_off_light, set_temperature, get_sensors_report, speak_via_yandex, run_script, activate_scene.
    - The bot routes commands like /ha_status or attempts to parse natural language if it looks like a light control.
    - Problem: Users feel management of HA is 'practically zero' and 'clunky'.
    - The bot runs on a server with Tailscale access to the local HA instance.

    GOAL: Leverage Gemini 3 capabilities (agentic Reasoning, multi-step planning) to make HA control feel 'magical' and proactive.
    """

    query = "Suggest a 'magical' smart home management architecture using Gemini 3. How can we use its deep reasoning to handle complex scenarios (e.g., 'Make it cozy for a movie', 'I'm leaving for 2 days', 'Why is it so hot in the living room?') instead of just simple entity toggles?"

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=query,
            config=GenerateContentConfig(
                system_instruction=context
            )
        )

        print("\n✨ Gemini 3 " + "Vision" if False else "Brain" + " Suggestions:")
        print(response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ask_gemini_3_for_ha_improvements()
