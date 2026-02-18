#!/usr/bin/env python3
import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add council to path
ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(ROOT_DIR / "LLM_Council"))

from council import LLMCouncil

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # Load AI Core env to get all keys and node URLs
    ai_core_env = ROOT_DIR / "Projects" / "AI_Core" / ".env"
    print(f"Loading env from {ai_core_env}")
    load_dotenv(ai_core_env, override=True)

    # Gather system context
    context_files = [
        ROOT_DIR / "SYSTEM_LOGIC.md",
        ROOT_DIR / "SYSTEM_MAP.md",
        ROOT_DIR / "System_Architecture_Vibranium.md",
        ROOT_DIR / "Management" / "UNIFIED_TASKS_2026-02-14.md",
        ROOT_DIR / "architecture" / "VASER_HUB.md"
    ]
    
    system_context = ""
    for cf in context_files:
        if cf.exists():
            system_context += f"\n--- FILE: {cf.name} ---\n"
            system_context += cf.read_text()
            system_context += "\n"

    query = f"""
Уважаемый Консилиум! 

Перед вами стоит задача "пропаять контакты" (system soldering) Единой Системы (Unified System Core). 
Вам предоставлен контекст её архитектуры, текущих задач и логики работы.

СИСТЕМНЫЙ КОНТЕКСТ:
{system_context}

ВАША ЗАДАЧА:
1. Проанализировать текущую структуру (AI Core, Content Factory, Bybit Bot, TokenBroker, Windows Node).
2. Выявить слабые места в синхронизации и передаче данных между узлами (Mac, Cloud, Windows).
3. Предложить финальную "сварку" (soldering) логики: как именно AI Core должен дирижировать остальными модулями в режиме "полный вперёд".
4. Сформировать "Картину" (The Picture) — единый, консолидированный план работы системы как автономного организма.

Chairman (Председатель) должен синтезировать ответы всех моделей в единый Vibranium-стандарт управления.
"""

    print("🚀 Initializing Council (Central Node + Cloud Backup)...")
    try:
        # Try using TokenBroker for real keys
        sys.path.append(str(ROOT_DIR / "Scripts" / "Utilities"))
        from token_broker import TokenBroker
        broker = TokenBroker()
        
        # We still need from_env for Ollama since TokenBroker might not have it mapped yet
        # or we can manually add providers
        providers = []
        
        # Load from TokenBroker
        gemini_key = broker.get_key("gemini")
        if gemini_key:
            from council.providers import GeminiProvider
            providers.append(GeminiProvider(api_key=gemini_key, model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")))
            print("✓ Gemini provider initialized via TokenBroker")

        openai_key = broker.get_key("openai")
        if openai_key:
            from council.providers import OpenAIProvider
            providers.append(OpenAIProvider(api_key=openai_key, model=os.getenv("OPENAI_MODEL", "gpt-4o")))
            print("✓ OpenAI provider initialized via TokenBroker")

        # Add Ollama (local Windows Node)
        ollama_url = os.getenv("OLLAMA_BASE_URL")
        if ollama_url:
            from council.providers import OllamaProvider
            providers.append(OllamaProvider(base_url=ollama_url, model=os.getenv("OLLAMA_MODEL", "llama3.2")))
            print(f"✓ Ollama provider initialized ({ollama_url})")

        if not providers:
            print("⚠️ No providers found via TokenBroker, falling back to from_env...")
            council = LLMCouncil.from_env()
        else:
            # Select chairman
            chairman = providers[0]
            for p in providers:
                if "gemini" in p.name:
                    chairman = p
                    break
            council = LLMCouncil(providers=providers, chairman=chairman)
        
        print(f"🏛️ Council Members: {[p.name for p in council.providers]}")
        print(f"👑 Chairman: {council.chairman.name}")
        
        print("\n🧐 Deliberation in progress... (this might take a minute)")
        session = await council.deliberate(query, verbose=True)
        
        print("\n" + "="*80)
        print("🏛️ COUNCIL CONSENSUS (THE PICTURE)")
        print("="*80)
        print(session.stage3_consensus)
        print("="*80)
        
        # Save output to a report
        output_path = ROOT_DIR / "Reports" / f"SYSTEM_SOLDERING_REPORT_{session.session_id}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report_content = f"# 🏛️ System Soldering Report (LLM Council)\n"
        report_content += f"Session ID: {session.session_id}\n"
        report_content += f"Date: {session.timestamp}\n\n"
        report_content += "## 👑 Consensus Result\n\n"
        report_content += session.stage3_consensus
        report_content += "\n\n## 📊 Internal Deliberations\n"
        
        for resp in session.stage1_responses:
            report_content += f"\n### {resp.provider_name} ({resp.model})\n"
            report_content += resp.content
            report_content += "\n"
            
        output_path.write_text(report_content)
        print(f"\n✅ Report saved to: {output_path}")

        await council.close()

    except Exception as e:
        logger.error(f"Council failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
