import sys
from pathlib import Path

# Setup paths
FACTORY_DIR = Path(__file__).parent.resolve()
PROJECTS_DIR = FACTORY_DIR.parent
AI_CORE_SRC = PROJECTS_DIR / "AI_Core/src"

if str(AI_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(AI_CORE_SRC))

try:
    from modules.knowledge_base import KnowledgeBase

    kb = KnowledgeBase()
    kb.connect()
    print("✅ Successfully connected to Knowledge Base from Content Factory context")
    kb.add_memory("ContentFactoryTest", {"status": "Integration OK"}, memory_type="test")
    print("✅ Test memory added")
except Exception as e:
    print(f"❌ Integration failed: {e}")
