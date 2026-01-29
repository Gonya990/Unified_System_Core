# Critical Issues Log

**Last Updated**: 2026-01-29
**Status**: Active Monitoring

---

## CRITICAL (P0) - Immediate Action Required

### 1. SECURITY: Hardcoded API Keys in Version Control

**File**: `Agent_Context/Knowledge_Base/Configs/docker-compose-unified-core.yaml`
**Lines**: 57-65

**Exposed Credentials**:
- `TELEGRAM_BOT_TOKEN` - Bot token exposed
- `GEMINI_API_KEY` - Google API key exposed
- `OPENAI_API_KEY` - OpenAI API key exposed (partial)

**Impact**: HIGH - Credentials can be harvested from git history
**Action Required**:
1. [ ] Rotate all three API keys immediately
2. [ ] Remove file from git history using `git filter-branch` or BFG Repo-Cleaner
3. [ ] Add file to `.gitignore` if it contains real secrets
4. [ ] Use environment variable substitution instead

**Owner**: Infrastructure Team
**Due**: ASAP

---

## HIGH (P1) - Fix Within 1 Week

### 2. ~~INFRA: Missing Dockerfiles for 5 Services~~ ✅ RESOLVED

**Issue**: Unified Docker Compose references services without Dockerfiles

| Service | Location | Status |
|---------|----------|--------|
| MCP Agent Mail Server | `Deployment/igor-gaming-1/mcp_agent_mail/` | Uses external repo |
| OpenAI MCP Gateway | `Scripts/openai_mcp_server/` | ✅ Dockerfile created |
| Antigravity MCP Server | `Agent_Context/Knowledge_Base/mcp-server/` | ✅ Dockerfile created |
| ChatKit Dashboard | `Projects/ChatKit_Dashboard/` | ✅ Dockerfile created |
| Connect Landing Page | `Projects/connect-landing-page/` | ✅ Dockerfile created |

**Impact**: Cannot deploy unified stack via Docker Compose
**Action Required**:
1. [x] Create Dockerfile for each service
2. [ ] Test builds locally
3. [ ] Update CI/CD to build and push images

**Resolution**: Created Dockerfiles on 2026-01-29. Updated Next.js configs with `output: 'standalone'`.

---

### 3. INFRA: Missing Kubernetes Secrets Template

**File**: `Projects/AI_Core/k8s/secrets.yaml`
**Referenced In**: `Projects/AI_Core/k8s/kustomization.yaml:9`

**Issue**: kustomization.yaml references `secrets.yaml` but only template exists
**Impact**: `kubectl apply -k .` will fail
**Action Required**:
1. [x] Created `secrets.yaml.template` with instructions
2. [ ] Update kustomization.yaml to not require secrets.yaml in repo
3. [ ] Document secret creation in deployment docs

---

### 4. CONFIG: Image Name Inconsistency

**Issue**: Different image names used across configurations

| Config | Image Name |
|--------|------------|
| `k8s/deployment.yaml` | `ghcr.io/gonya990/ai-telegram-bot` |
| `docker-compose.yml` | `ghcr.io/gonya990/unified_system_core/ai-telegram-bot` |

**Impact**: Confusion, potential deployment failures
**Action Required**:
1. [ ] Standardize on single image name format
2. [ ] Update all manifests to use consistent naming
3. [ ] Update CI/CD pipeline if needed

---

## MEDIUM (P2) - Fix Within 2 Weeks

### 5. ~~CONFIG: Deprecated Docker Compose Version Syntax~~ ✅ RESOLVED

**Files**:
- `Projects/AI_Core/docker-compose.dev.yml` - ✅ Fixed
- `Deployment/igor-gaming-1/mcp_agent_mail/docker-compose.yml` - ✅ Fixed

**Issue**: `version` key is deprecated in Docker Compose V2
**Impact**: Warning messages, potential future compatibility issues
**Action Required**:
1. [x] Remove `version:` line from all docker-compose files

**Resolution**: Removed deprecated version keys on 2026-01-29.

---

### 6. CONFIG: Missing Health Checks in Docker Compose

**Files**: Multiple docker-compose.yml files

**Services Without Health Checks**:
- `mcp_agent_mail/docker-compose.yml` - db service
- `mcp_agent_mail/docker-compose.yml` - server service

**Impact**: Docker cannot determine service health, affects depends_on
**Action Required**:
1. [ ] Add health checks to all services
2. [ ] Use `condition: service_healthy` in depends_on

---

### 7. INFRA: Hardcoded User Paths in Systemd Services

**Files**:
- `infra/ai-bot.service` - Lines 8,10,15,17,18
- `infra/mail-processor.service` - Lines 8,9,12

**Issue**: Paths hardcoded to `/home/gonya/Documents/...`
**Impact**: Services won't work on different systems
**Action Required**:
1. [ ] Parameterize paths using environment variables
2. [ ] Create template service files
3. [ ] Document customization process

---

### 8. CONFIG: Default Password Fallbacks

**File**: `Deployment/igor-gaming-1/mcp_agent_mail/docker-compose.yml`

**Issue**: Default passwords used as fallbacks:
```yaml
POSTGRES_PASSWORD: ${DATABASE_PASSWORD:-agent_pass}
HTTP_BEARER_TOKEN: ${AUTH_TOKEN:-antigravity_secret}
```

**Impact**: Insecure defaults if environment variables not set
**Action Required**:
1. [ ] Remove default fallbacks
2. [ ] Require explicit environment variable setting
3. [ ] Add validation in entrypoint scripts

---

## LOW (P3) - Track for Future

### 9. MISSING: No Horizontal Pod Autoscaler

**Location**: `Projects/AI_Core/k8s/`
**Issue**: No HPA defined for auto-scaling
**Impact**: Cannot scale based on load

---

### 10. MISSING: No Network Policies

**Location**: `Projects/AI_Core/k8s/`
**Issue**: No Kubernetes NetworkPolicy resources
**Impact**: No network segmentation between pods

---

### 11. MISSING: No Pod Disruption Budget

**Location**: `Projects/AI_Core/k8s/`
**Issue**: No PDB defined
**Impact**: No availability guarantees during maintenance

---

### 12. MISSING: No Resource Quotas

**Location**: `infra/k8s/`
**Issue**: No ResourceQuota in namespaces
**Impact**: Runaway pods could consume cluster resources

---

## Resolved Issues

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-01-29 | Missing secrets.yaml.template | Created template with documentation |
| 2026-01-29 | No unified Docker Compose | Created `infra/docker-compose.unified.yml` |
| 2026-01-29 | Missing K8s manifests for services | Created manifests in `infra/k8s/` |
| 2026-01-29 | Missing Dockerfiles for 5 services | Created Dockerfiles + updated Next.js configs |
| 2026-01-29 | Deprecated Docker Compose version keys | Removed `version:` from 2 files |
| 2026-01-29 | No deployment validation tools | Created `infra/scripts/` + Makefile |

---

## Issue Tracking Workflow

1. **Add new issues** in appropriate severity section
2. **Update status** with checkboxes as work progresses
3. **Move to Resolved** when fixed with date and resolution
4. **Review weekly** to reprioritize as needed

**Severity Definitions**:
- **P0 CRITICAL**: Security issues, data loss risk, production down
- **P1 HIGH**: Major functionality blocked, affects multiple users
- **P2 MEDIUM**: Important but workaround exists
- **P3 LOW**: Nice to have, future improvement
