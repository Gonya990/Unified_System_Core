# Implementation Plan: Hybrid AI Agent System

## Goal

Build a comprehensive AI agent system combining:

- **RAG**: Local vector database for project knowledge
- **Function Calling**: Dynamic n8n workflow invocation
- **Enhanced Browser Agent**: Documentation-aware automation

## User Review Required

> [!IMPORTANT]
> **Architecture Decision**: This implementation will create a unified agent that can:
>
> - Search through project documentation semantically
> - Execute n8n workflows on demand
> - Make intelligent browser automation decisions
>
> **Cost Implications**:
>
> - ChromaDB: Free (local)
> - Gemini API calls: ~$0.001-0.005 per request
> - n8n: Already running (no additional cost)
>
> **Storage**: ~500MB for vector database

---

## Proposed Changes

### Component 1: Local RAG System

#### [NEW] [`rag_system/`](file:///home/gonya/01_Projects/PRJ-004_AI_Agents/02_Dev/rag_system/)

**Purpose**: Semantic search over project documentation

**Files to create**:

- `vector_store.py` - ChromaDB wrapper
- `document_loader.py` - Ingests .md, .py, .txt files
- `embeddings.py` - Vertex AI Embeddings integration
- `search.py` - Semantic search interface

**Key features**:

```python
# Example usage
rag = RAGSystem()
rag.index_directory("/home/gonya/01_Projects/PRJ-004_AI_Agents/")
results = rag.search("How to connect to remote Chrome?")
# Returns: Relevant snippets from browser_agent.py and docs
```

---

### Component 2: Function Calling System

#### [NEW] [`function_calling/`](file:///home/gonya/01_Projects/PRJ-004_AI_Agents/02_Dev/function_calling/)

**Purpose**: Enable Gemini to invoke n8n workflows and system commands

**Files to create**:

- `function_registry.py` - Available functions catalog
- `n8n_client.py` - n8n API wrapper
- `executor.py` - Function execution handler
- `schemas.py` - Function definitions for Gemini

**Available functions**:

```python
functions = [
    {
        "name": "check_docker_status",
        "description": "Check status of Docker containers",
        "parameters": {"container_name": "optional"}
    },
    {
        "name": "execute_n8n_workflow",
        "description": "Trigger n8n workflow by name",
        "parameters": {"workflow_name": "required"}
    },
    {
        "name": "search_documentation",
        "description": "Search project docs via RAG",
        "parameters": {"query": "required"}
    }
]
```

---

### Component 3: Enhanced Browser Agent

#### [MODIFY] [`browser_agent.py`](file:///home/gonya/01_Projects/PRJ-004_AI_Agents/02_Dev/browser_agent.py)

**Changes**:

1. Add RAG context injection
2. Integrate function calling
3. Hybrid decision engine (Ollama → Gemini + RAG)
4. Documentation-aware prompts

**New architecture**:

```python
async def make_decision(goal, page_content):
    # 1. Search documentation for relevant context
    context = rag.search(goal)
    
    # 2. Try local Ollama first (fast)
    try:
        response = await ask_ollama(goal, page_content, context)
        if response.confidence > 0.8:
            return response
    except TimeoutError:
        pass
    
    # 3. Fallback to Gemini with function calling
    response = await ask_gemini_with_functions(
        goal, 
        page_content, 
        context,
        available_functions
    )
    
    # 4. Execute function if needed
    if response.function_call:
        result = await execute_function(response.function_call)
        return await ask_gemini(goal, result)
    
    return response
```

---

### Component 4: Unified API

#### [NEW] [`hybrid_agent.py`](file:///home/gonya/01_Projects/PRJ-004_AI_Agents/02_Dev/hybrid_agent.py)

**Purpose**: Single entry point for all agent capabilities

```python
agent = HybridAgent()

# Use RAG
answer = agent.ask("How do I configure Tailscale?")

# Execute workflow
result = agent.execute("Check all Docker containers")

# Browse with context
agent.browse("Go to Google Cloud Console and download credentials")
```

---

## Verification Plan

### Automated Tests

1. **RAG System Test**

```bash
python3 -m pytest tests/test_rag.py
# Verify: Document indexing, semantic search accuracy
```

2. **Function Calling Test**

```bash
python3 -m pytest tests/test_functions.py
# Verify: n8n workflow execution, Docker commands
```

3. **Browser Agent Test**

```bash
python3 test_enhanced_browser.py
# Verify: Context-aware navigation, function integration
```

### Manual Verification

1. **End-to-End Workflow**
   - Ask agent: "Check if Chrome container is running, if not start it"
   - Expected: RAG finds Docker docs → Function calls docker ps → Executes docker start if needed

2. **Documentation Search**
   - Query: "What's the Tailscale IP of Windows node?"
   - Expected: Returns `100.127.194.111` from walkthrough.md

3. **Hybrid Browser Automation**
   - Command: "Navigate to n8n dashboard and show active workflows"
   - Expected: Uses RAG context → Opens browser → Extracts workflow list

---

## Implementation Phases

### Phase 1: Foundation (2-3 hours)

- Install ChromaDB
- Create basic RAG system
- Index existing documentation

### Phase 2: Function Calling (1-2 hours)

- Define function schemas
- Build n8n client
- Test workflow execution

### Phase 3: Integration (2-3 hours)

- Enhance browser_agent.py
- Build hybrid decision engine
- Create unified API

### Phase 4: Testing & Optimization (1-2 hours)

- Write tests
- Optimize performance
- Document usage

**Total estimated time**: 6-10 hours
**Complexity**: Medium-High
**Risk**: Low (all components can be tested independently)

---

## Dependencies

### Python Packages

```bash
pip install chromadb sentence-transformers google-cloud-aiplatform httpx pytest
```

### System Requirements

- Disk space: ~500MB for vector DB
- RAM: ~2GB additional for embeddings
- Network: Access to Vertex AI Embeddings API

---

## Success Criteria

- [ ] RAG system indexes 100+ documents
- [ ] Search returns relevant results in <1s
- [ ] Function calling executes n8n workflows successfully
- [ ] Browser agent makes context-aware decisions
- [ ] Hybrid system reduces Gemini API calls by 50%
- [ ] End-to-end latency <5s for complex queries

---

## Rollback Plan

If issues arise:

1. RAG system is optional - can disable without breaking existing functionality
2. Function calling is additive - browser agent works without it
3. All changes are in new files - easy to revert

**Recommendation**: Proceed with implementation in phases, testing each component independently.
