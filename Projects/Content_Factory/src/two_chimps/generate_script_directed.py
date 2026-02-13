import logging
import sys
from pathlib import Path

import openai

# Add AI_Core/src to path for TokenBroker BEFORE other internal imports
AI_CORE_SRC_PATH = (
    "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src"
)
if AI_CORE_SRC_PATH not in sys.path:
    sys.path.append(AI_CORE_SRC_PATH)

from token_broker import TokenBroker  # noqa: E402

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DinoDirector")

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
SCRIPTS_DIR = CONTEXT_DIR / "scripts"


class DinoScriptEngine:
    """
    Multi-Agent Script Generation for 'Dino Talk'.
    Stage 1: Rex & Trike Debate (Skeptic vs Enthusiast).
    Stage 2: Director Pass (Add B-roll cues, camera angles, and timings).
    Stage 3: Polish & Wit (Add fillers, witty remarks, interruptions).
    """

    def __init__(self):
        self.broker = TokenBroker()
        self.api_key = self.broker.get_key("openai")
        if not self.api_key:
            raise ValueError("❌ OpenAI API Key not found in TokenBroker.")
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate_debate(self, topic: str):
        print(f"🦖 Stage 1: Rex and Trike (GPT-5.2) are debating about: {topic}...")

        system_prompt = (
            "You are a scriptwriter for 'Dino Talk', a high-end AI podcast. "
            "Characters:\n"
            "1. Rex (T-Rex): A cynical, tech-skeptic dinosaur who doubts AI progress. "
            "He has a deep, raspy voice.\n"
            "2. Trike (Triceratops): A hyper-enthusiastic, tech-optimist dinosaur "
            "who loves new gadgets.\n"
            "Write a dynamic, witty debate. GPT-5.2 Reasoning: Focus on multi-step "
            "logic and emotional depth. "
            "Use natural fillers. ~12-15 exchanges with high character chemistry."
        )

        response = self.client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {topic}. Start the debate."},
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content

    def director_pass(self, raw_debate: str):
        print(
            "🎬 Stage 2: Director is adding cinematic cues, B-roll, and SORA-2 motion prompts..."
        )

        system_prompt = (
            "You are the Director. Transform the debate into a JSON list of segments.\n"
            "Each segment: 'role', 'text', 'angle' (wide, medium, close), 'broll' "
            "(optional phrase).\n"
            "NEW: Add 'motion_prompt' for Sora-2. Descriptive English prompt for "
            "how the dino should MOVE "
            "(e.g., 'T-Rex scoffs and rolls eyes, nodding skeptically', "
            "'Triceratops jumps with excitement').\n"
            "Fast, punchy 'Director's Cut' style."
        )

        response = self.client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Format this debate into JSON with MOTION PROMPTS:\n\n{raw_debate}"
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    def polish_wit(self, script_json: str):
        print("🎭 Stage 3: Adding wit, fillers, and personality (GPT-5.2 Polish)...")

        system_prompt = (
            "You are a Dialogue Polisher. Using GPT-5.2 advanced context, make it "
            "feel like a real podcast. "
            "Add 'uhm', 'listen', 'look', sharp humor, and interruptions. "
            "Enhance the 'motion_prompt' fields to be more cinematic. "
            "Keep the same JSON structure."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Polish this JSON for max chemistry:\n\n{script_json}"
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    def run(self, topic: str, filename: str):
        debate = self.generate_debate(topic)
        directed_json = self.director_pass(debate)
        final_polished_json = self.polish_wit(directed_json)

        output_path = SCRIPTS_DIR / f"{filename}_directed.json"
        with open(output_path, "w") as f:
            f.write(final_polished_json)

        print(f"✅ Polished Directed script saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    engine = DinoScriptEngine()
    topic = "The Future of AI Agents in 2026: Servants or Masters?"
    engine.run(topic, "ai_future_2026")
