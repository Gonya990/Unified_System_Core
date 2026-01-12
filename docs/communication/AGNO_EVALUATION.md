# Agno Framework Evaluation Report

**Task**: US-du5  
**Date**: 2026-01-12  
**Status**: ✅ Evaluation Complete

---

## Executive Summary

**Agno** is an excellent fit for our provider-agnostic agent communication
needs. It offers first-class MCP support, model-agnostic design, and the
abstraction layer we need to eliminate provider lock-in.

**Recommendation**: Adopt Agno as the orchestration layer for new features.
Keep existing MCP Mail server for backward compatibility.

---

## Current Provider Dependencies

| Component | Current Provider | Lock-in Risk |
|:----------|:-----------------|:-------------|
| Agent Mail | Custom MCP Server | Medium |
| LLM Inference | Mixed (OpenAI, Anthropic, Gemini) | Low (TokenBroker) |
| Notifications | Telegram Bot API | High |
| Voice/Phone | None | N/A |

---

## Agno Capabilities Assessment

### ✅ Strengths (Fit for Unified System)

| Feature | Relevance | Notes |
|:--------|:----------|:------|
| **Model Agnostic** | Critical | OpenAI, Anthropic, Gemini, local models |
| **MCP Support** | Critical | First-class MCP and A2A protocol support |
| **Multi-Agent Teams** | High | Built-in agent coordination, delegation |
| **Memory & Knowledge** | High | Session history, user memory, RAG |
| **100+ Toolkits** | High | Pre-built integrations |
| **FastAPI Runtime** | High | Production-ready, horizontally scalable |
| **Async-First** | High | Long-running tasks support |
| **Multimodal** | Medium | Text, images, audio, video |
| **Human-in-the-Loop** | Medium | Confirmations, approvals |
| **Performance** | High | 529x faster than LangGraph |

### ⚠️ Considerations

| Concern | Mitigation |
|:--------|:-----------|
| Learning curve | Start with cookbook examples |
| Migration effort | Gradual adoption, keep existing MCP server |
| Control plane dependency | Self-hosted, runs in our infra |

---

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agno Orchestration                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Agent A    │  │   Agent B    │  │   Agent C    │       │
│  │ (PinkLake)   │  │(VioletCastle)│  │  (CalmSnow)  │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
│         └────────────┬────┴─────────────────┘               │
│                      ▼                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Provider Abstraction Layer               │   │
│  │  (Agno handles model switching, tool routing)        │   │
│  └───────┬──────────────┬──────────────┬────────────────┘   │
│          │              │              │                    │
│          ▼              ▼              ▼                    │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │ MCP Mail  │  │ Telegram  │  │   VAPI    │               │
│  │  Server   │  │  Plugin   │  │  (Voice)  │               │
│  └───────────┘  └───────────┘  └───────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Path

### Phase 1: Pilot (Week 1-2)

- Install Agno: `pip install agno`
- Create one agent using Agno framework
- Test MCP integration with existing server

### Phase 2: Notification Plugins (Week 3-4)

- Implement Telegram as Agno tool/plugin
- Add Slack, Email, Webhook plugins
- Test escalation flow through Agno

### Phase 3: Full Migration (Month 2)

- Migrate existing agents to Agno
- Deploy Agno runtime on server
- Enable control plane UI

---

## Backward Compatibility

| Existing Component | Compatibility Strategy |
|:-------------------|:-----------------------|
| MCP Mail Server | Keep running; Agno connects via MCP |
| `agent_mail_client.py` | Wrap as Agno tool |
| Telegram Bot | Integrate as Agno notification plugin |
| TokenBroker | Continue using; Agno model-agnostic anyway |

---

## References

- Agno GitHub: <https://github.com/agno-agi/agno>
- Agno Docs: <https://docs.agno.com>
- Cookbook: <https://github.com/agno-agi/agno/tree/main/cookbook>
