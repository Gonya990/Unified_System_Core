# Deployment Configuration Review

**Date**: 2026-01-29
**Branch**: `claude/review-deployment-configs-Xm28T`

---

## Executive Summary

This document reviews all deployment configurations in the Unified System Core repository, including Kubernetes manifests, Docker Compose files, systemd services, and CI/CD pipelines. It identifies issues, proposes improvements, and provides unified deployment plans for all discoverable services.

---

## 1. Inventory of Deployable Services

| # | Service | Location | Technology | Current Deployment Method |
|---|---------|----------|------------|---------------------------|
| 1 | AI Telegram Bot | `Projects/AI_Core/` | Python 3.12 | Docker, K8s, systemd |
| 2 | Bridge Server | `Projects/AI_Core/src/bridge_server.py` | FastAPI | Part of AI Bot container |
| 3 | MCP Mail Processor | `Scripts/Orchestration/mail_processor.py` | Python | systemd only |
| 4 | Agent Mail Server | `Deployment/igor-gaming-1/mcp_agent_mail/` | Python + PostgreSQL | Docker Compose |
| 5 | OpenAI MCP Gateway | `Scripts/openai_mcp_server/` | FastMCP | None |
| 6 | CLIProxyAPI | `infra/cliproxyapi/` | Custom | Docker Compose |
| 7 | ChatKit Dashboard | `Projects/ChatKit_Dashboard/` | Next.js | None |
| 8 | Connect Landing Page | `Projects/connect-landing-page/` | Next.js | None |
| 9 | Antigravity MCP Server | `Agent_Context/Knowledge_Base/mcp-server/` | Node.js | systemd |
| 10 | Ollama (LLM inference) | External | Go | Docker |
| 11 | Open WebUI | External | Python | Docker |

---

## 2. Existing Configuration Review

### 2.1 Kubernetes Manifests (AI Core)

**Location**: `Projects/AI_Core/k8s/`

**Files**:
- `namespace.yaml` - Creates `telegram-bot` namespace
- `configmap.yaml` - Environment configuration
- `deployment.yaml` - Main bot deployment
- `service.yaml` - ClusterIP service for health checks
- `pvc.yaml` - 1Gi persistent volume
- `kustomization.yaml` - Kustomize overlay
- `argocd-application.yaml` - GitOps deployment

**Assessment**: ✅ Well-structured

| Aspect | Rating | Notes |
|--------|--------|-------|
| Resource Limits | ✅ Good | 128Mi-512Mi memory, 100m-500m CPU |
| Health Probes | ✅ Good | Liveness + Readiness on `/health` and `/ready` |
| Rolling Updates | ✅ Good | maxUnavailable: 0, maxSurge: 1 |
| Labels | ✅ Good | app.kubernetes.io/* labels present |
| GitOps | ✅ Good | ArgoCD with auto-sync, self-heal, prune |
| Secrets | ⚠️ OK | External secretRef (must be created manually) |

**Issues Found**:
1. **Missing secrets.yaml template** - Referenced in kustomization.yaml but not in repo
2. **Image mismatch** - deployment.yaml uses `ghcr.io/gonya990/ai-telegram-bot` but docker-compose uses `ghcr.io/gonya990/unified_system_core/ai-telegram-bot`
3. **No HPA** - No Horizontal Pod Autoscaler defined
4. **No NetworkPolicy** - No network segmentation
5. **No PodDisruptionBudget** - No availability guarantees during maintenance

---

### 2.2 Docker Compose Configurations

#### 2.2.1 AI Core Production (`Projects/AI_Core/docker-compose.yml`)

**Assessment**: ✅ Good with minor issues

| Aspect | Rating | Notes |
|--------|--------|-------|
| YAML Anchors | ✅ Good | Uses `x-ai-bot-common` for DRY |
| Watchtower | ✅ Good | Auto-updates enabled |
| Logging | ✅ Good | json-file with rotation |
| Volume Mounts | ⚠️ Complex | Many bind mounts - fragile |
| Secrets | ⚠️ Partial | Uses Docker secrets for watchtower |

**Issues**:
1. Hardcoded GCP project ID in environment
2. Many relative path volume mounts (fragile)
3. No network isolation defined

#### 2.2.2 AI Core Dev (`Projects/AI_Core/docker-compose.dev.yml`)

**Assessment**: ⚠️ Outdated

- Uses deprecated `version: "3.8"` syntax
- Named volume `bot-data` declared but not used
- Missing env_file reference

#### 2.2.3 Agent Mail Server (`Deployment/igor-gaming-1/mcp_agent_mail/docker-compose.yml`)

**Assessment**: ✅ Good

- PostgreSQL 16 Alpine with proper credentials
- Async database URL configuration
- Proper volume persistence

**Issues**:
1. Uses deprecated `version: "3.8"` syntax
2. No health checks defined
3. No restart policy on server service
4. Default password fallbacks are security risk

#### 2.2.4 CLIProxyAPI (`infra/cliproxyapi/docker-compose.yml`)

**Assessment**: ✅ Good

- External network integration
- Watchtower auto-updates
- Clean configuration

#### 2.2.5 Unified Core Template (`Agent_Context/Knowledge_Base/Configs/docker-compose-unified-core.yaml`)

**Assessment**: ❌ CRITICAL SECURITY ISSUE

```yaml
# EXPOSED SECRETS IN FILE:
- TELEGRAM_BOT_TOKEN=8518131338:AAGp4GpyNR0S-Dq3bwzD0rPkZN0sEcBLaB0
- GEMINI_API_KEY=AIzaSyBVtb9sY7MMiKWkpcQAEkvLST86yr9O1n4
- OPENAI_API_KEY=sk-proj-tBRH9G7RWRAu0x6RMhNUZeqqr_fFYe...
```

**IMMEDIATE ACTION REQUIRED**:
1. Rotate all exposed API keys
2. Remove hardcoded secrets from version control
3. Use environment variable substitution or secrets management

---

### 2.3 Systemd Services

#### 2.3.1 AI Bot (`infra/ai-bot.service`)

**Assessment**: ⚠️ Functional but basic

- Hardcoded paths to `/home/gonya/Documents/Unified_System/`
- Logs to file instead of journal
- No resource limits (MemoryMax, CPUQuota)
- No watchdog integration

#### 2.3.2 Mail Processor (`infra/mail-processor.service`)

**Assessment**: ⚠️ Nix-specific

- Uses `/run/current-system/sw/bin/bash` (NixOS only)
- Uses `devenv shell` wrapper (complex dependency)
- Logs to journal (good)

---

### 2.4 CI/CD Pipeline (`.github/workflows/build.yml`)

**Assessment**: ✅ Excellent

| Feature | Status |
|---------|--------|
| Multi-arch build | ✅ Docker Buildx |
| Security scanning | ✅ Trivy vulnerability scanner |
| SBOM/Provenance | ✅ Attestation enabled |
| Cache optimization | ✅ GHA cache |
| Auto-tag update | ✅ Updates kustomization.yaml |
| Concurrency control | ✅ Cancel-in-progress |

---

## 3. Security Issues Summary

| Severity | Issue | Location | Status |
|----------|-------|----------|--------|
| 🔴 CRITICAL | Hardcoded API keys | `docker-compose-unified-core.yaml` | Needs rotation |
| 🟡 HIGH | No secrets template | `k8s/secrets.yaml` | Missing |
| 🟡 MEDIUM | Default password fallbacks | `mcp_agent_mail/docker-compose.yml` | Should require |
| 🟢 LOW | Hardcoded user paths | `infra/*.service` | Improve portability |

---

## 4. Recommendations

### 4.1 Immediate Actions

1. **Rotate compromised API keys** in `docker-compose-unified-core.yaml`
2. **Add `.gitignore` entries** for any local `.env` files with secrets
3. **Create secrets template** for Kubernetes deployment

### 4.2 Short-term Improvements

1. **Standardize image naming**: Use `ghcr.io/gonya990/unified_system_core/<service>:tag`
2. **Remove deprecated version syntax** from Docker Compose files
3. **Add health checks** to all Docker Compose services
4. **Create unified network** for inter-service communication

### 4.3 Long-term Architecture

1. **Expand Kubernetes manifests** for all services
2. **Implement Helm charts** for parameterized deployments
3. **Add monitoring stack** (Prometheus, Grafana)
4. **Implement GitOps** for all services via ArgoCD

---

## 5. Proposed Unified Deployment Configurations

See accompanying files:
- `infra/docker-compose.unified.yml` - Unified Docker Compose for all services
- `infra/k8s/` - Kubernetes manifests for additional services

---

## 6. Service Port Mapping

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| AI Telegram Bot | 8080 | HTTP | Health checks |
| AI Telegram Bot | 8090 | HTTP | Bridge API |
| AI Telegram Bot | 8095 | HTTP | Dashboard |
| AI Telegram Bot | 8096 | HTTP | Additional API |
| Agent Mail Server | 8765 | HTTP | MCP API |
| CLIProxyAPI | 8317 | HTTP | CLI Proxy |
| OpenAI MCP Gateway | 8766 | HTTP | MCP API |
| ChatKit Dashboard | 3001 | HTTP | Web UI |
| Connect Landing | 3000 | HTTP | Web UI |
| Antigravity MCP | 3005 | HTTP | MCP API |
| Ollama | 11434 | HTTP | LLM API |
| Open WebUI | 3000 | HTTP | Chat UI |
| PostgreSQL | 5432 | TCP | Database |

---

## 7. Deployment Methods Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Docker Compose** | Development, Single-node | Simple, fast iteration | No HA, manual scaling |
| **Kubernetes** | Production, Multi-node | HA, auto-scaling, GitOps | Complex, resource overhead |
| **systemd** | Bare metal, Edge | No container overhead | Manual updates, no isolation |
