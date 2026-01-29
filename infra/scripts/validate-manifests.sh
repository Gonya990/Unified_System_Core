#!/usr/bin/env bash
# Validate Kubernetes Manifests and Docker Compose Files
# Run this script to check all deployment configurations

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo "========================================"
echo "  Deployment Configuration Validator"
echo "========================================"
echo ""

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# =============================================================================
# 1. Check required tools
# =============================================================================
echo "1. Checking required tools..."
echo "---"

if command -v docker &> /dev/null; then
    check_pass "Docker installed: $(docker --version | head -1)"
else
    check_warn "Docker not installed (required for builds)"
fi

if command -v kubectl &> /dev/null; then
    check_pass "kubectl installed: $(kubectl version --client -o json 2>/dev/null | grep -o '"gitVersion": "[^"]*"' | head -1)"
else
    check_warn "kubectl not installed (required for K8s deployments)"
fi

if command -v kustomize &> /dev/null; then
    check_pass "kustomize installed"
else
    check_warn "kustomize not installed (kubectl has built-in kustomize)"
fi

echo ""

# =============================================================================
# 2. Validate Kubernetes Manifests
# =============================================================================
echo "2. Validating Kubernetes manifests..."
echo "---"

K8S_DIRS=(
    "$ROOT_DIR/Projects/AI_Core/k8s"
    "$ROOT_DIR/infra/k8s"
)

for K8S_DIR in "${K8S_DIRS[@]}"; do
    if [[ -d "$K8S_DIR" ]]; then
        echo "  Checking: ${K8S_DIR#$ROOT_DIR/}"

        # Check YAML syntax
        for yaml_file in "$K8S_DIR"/*.yaml "$K8S_DIR"/*.yml; do
            if [[ -f "$yaml_file" ]]; then
                filename=$(basename "$yaml_file")

                # Skip templates
                if [[ "$filename" == *".template"* ]]; then
                    check_warn "  $filename (template - skipped)"
                    continue
                fi

                # Validate YAML syntax
                if python3 -c "import yaml; yaml.safe_load(open('$yaml_file'))" 2>/dev/null; then
                    check_pass "  $filename (valid YAML)"
                else
                    check_fail "  $filename (invalid YAML syntax)"
                fi
            fi
        done

        # Validate kustomization
        if [[ -f "$K8S_DIR/kustomization.yaml" ]]; then
            if command -v kubectl &> /dev/null; then
                if kubectl kustomize "$K8S_DIR" > /dev/null 2>&1; then
                    check_pass "  kustomization.yaml (builds successfully)"
                else
                    check_fail "  kustomization.yaml (build failed)"
                fi
            fi
        fi
    else
        check_warn "Directory not found: ${K8S_DIR#$ROOT_DIR/}"
    fi
done

echo ""

# =============================================================================
# 3. Validate Docker Compose Files
# =============================================================================
echo "3. Validating Docker Compose files..."
echo "---"

COMPOSE_FILES=(
    "$ROOT_DIR/Projects/AI_Core/docker-compose.yml"
    "$ROOT_DIR/Projects/AI_Core/docker-compose.dev.yml"
    "$ROOT_DIR/infra/docker-compose.unified.yml"
    "$ROOT_DIR/infra/cliproxyapi/docker-compose.yml"
    "$ROOT_DIR/Deployment/igor-gaming-1/mcp_agent_mail/docker-compose.yml"
)

for compose_file in "${COMPOSE_FILES[@]}"; do
    if [[ -f "$compose_file" ]]; then
        filename="${compose_file#$ROOT_DIR/}"

        # Check YAML syntax
        if python3 -c "import yaml; yaml.safe_load(open('$compose_file'))" 2>/dev/null; then
            # Check for deprecated version key
            if grep -q "^version:" "$compose_file"; then
                check_warn "$filename (deprecated 'version:' key)"
            else
                check_pass "$filename (valid)"
            fi

            # Validate with docker compose if available
            if command -v docker &> /dev/null; then
                if docker compose -f "$compose_file" config > /dev/null 2>&1; then
                    check_pass "$filename (docker compose validated)"
                else
                    check_warn "$filename (docker compose validation failed - may need env vars)"
                fi
            fi
        else
            check_fail "$filename (invalid YAML syntax)"
        fi
    else
        check_warn "File not found: ${compose_file#$ROOT_DIR/}"
    fi
done

echo ""

# =============================================================================
# 4. Verify Dockerfiles exist for services
# =============================================================================
echo "4. Verifying Dockerfiles for services..."
echo "---"

DOCKERFILE_LOCATIONS=(
    "Projects/AI_Core/Dockerfile"
    "Scripts/openai_mcp_server/Dockerfile"
    "Agent_Context/Knowledge_Base/mcp-server/Dockerfile"
    "Projects/ChatKit_Dashboard/Dockerfile"
    "Projects/connect-landing-page/Dockerfile"
    "infra/Dockerfile.mail-processor"
)

for dockerfile in "${DOCKERFILE_LOCATIONS[@]}"; do
    filepath="$ROOT_DIR/$dockerfile"
    if [[ -f "$filepath" ]]; then
        check_pass "$dockerfile"
    else
        check_fail "$dockerfile (missing)"
    fi
done

echo ""

# =============================================================================
# 5. Check environment templates
# =============================================================================
echo "5. Checking environment templates..."
echo "---"

ENV_TEMPLATES=(
    "$ROOT_DIR/.env.example"
    "$ROOT_DIR/infra/.env.example"
    "$ROOT_DIR/Projects/AI_Core/.env.example"
)

for env_file in "${ENV_TEMPLATES[@]}"; do
    filename="${env_file#$ROOT_DIR/}"
    if [[ -f "$env_file" ]]; then
        check_pass "$filename"
    else
        check_warn "$filename (missing - may need documentation)"
    fi
done

echo ""

# =============================================================================
# 6. Check for hardcoded secrets (security scan)
# =============================================================================
echo "6. Security scan for hardcoded secrets..."
echo "---"

SECRET_PATTERNS=(
    "sk-proj-"      # OpenAI API key
    "sk-ant-"       # Anthropic API key
    "AIzaSy"        # Google API key
    "ghp_"          # GitHub PAT
    "ghs_"          # GitHub App token
)

SCAN_DIRS=(
    "$ROOT_DIR/infra"
    "$ROOT_DIR/Projects"
    "$ROOT_DIR/Agent_Context/Knowledge_Base/Configs"
)

for dir in "${SCAN_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        for pattern in "${SECRET_PATTERNS[@]}"; do
            matches=$(grep -r --include="*.yaml" --include="*.yml" --include="*.json" -l "$pattern" "$dir" 2>/dev/null || true)
            if [[ -n "$matches" ]]; then
                while IFS= read -r match; do
                    relative_path="${match#$ROOT_DIR/}"
                    check_fail "SECURITY: Potential secret found in $relative_path (pattern: $pattern...)"
                done <<< "$matches"
            fi
        done
    fi
done

if [[ $ERRORS -eq 0 ]] && [[ ! $(grep -r --include="*.yaml" --include="*.yml" -E "(sk-proj-|AIzaSy|ghp_)" "$ROOT_DIR/infra" "$ROOT_DIR/Projects" 2>/dev/null) ]]; then
    check_pass "No hardcoded secrets detected in scanned directories"
fi

echo ""

# =============================================================================
# Summary
# =============================================================================
echo "========================================"
echo "  Validation Summary"
echo "========================================"
echo ""
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}Validation FAILED${NC} - Please fix errors before deployment"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}Validation PASSED with warnings${NC}"
    exit 0
else
    echo -e "${GREEN}Validation PASSED${NC}"
    exit 0
fi
