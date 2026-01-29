#!/usr/bin/env bash
# Test Docker Builds for All Services
# Run this script to verify all Dockerfiles build successfully

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
DRY_RUN=false
VERBOSE=false
SPECIFIC_SERVICE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --verbose|-v) VERBOSE=true; shift ;;
        --service) SPECIFIC_SERVICE="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run     Show what would be built without building"
            echo "  --verbose,-v  Show build output"
            echo "  --service X   Only build specific service"
            echo "  --help,-h     Show this help"
            echo ""
            echo "Services:"
            echo "  ai-telegram-bot, openai-mcp-gateway, antigravity-mcp,"
            echo "  chatkit-dashboard, connect-landing, mail-processor"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "========================================"
echo "  Docker Build Test Suite"
echo "========================================"
echo ""

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Service definitions: name|context|dockerfile|tag
SERVICES=(
    "ai-telegram-bot|Projects/AI_Core|Dockerfile|test-ai-bot:latest"
    "openai-mcp-gateway|Scripts/openai_mcp_server|Dockerfile|test-openai-mcp:latest"
    "antigravity-mcp|Agent_Context/Knowledge_Base/mcp-server|Dockerfile|test-antigravity-mcp:latest"
    "chatkit-dashboard|Projects/ChatKit_Dashboard|Dockerfile|test-chatkit:latest"
    "connect-landing|Projects/connect-landing-page|Dockerfile|test-connect:latest"
    "mail-processor|.|infra/Dockerfile.mail-processor|test-mail-processor:latest"
)

PASS=0
FAIL=0
SKIP=0

for service_def in "${SERVICES[@]}"; do
    IFS='|' read -r name context dockerfile tag <<< "$service_def"

    # Skip if specific service requested and this isn't it
    if [[ -n "$SPECIFIC_SERVICE" ]] && [[ "$SPECIFIC_SERVICE" != "$name" ]]; then
        continue
    fi

    context_path="$ROOT_DIR/$context"
    dockerfile_path="$ROOT_DIR/$context/$dockerfile"

    # Handle mail-processor special case
    if [[ "$name" == "mail-processor" ]]; then
        context_path="$ROOT_DIR"
        dockerfile_path="$ROOT_DIR/$dockerfile"
    fi

    echo -e "${BLUE}Building: $name${NC}"
    echo "  Context:    $context"
    echo "  Dockerfile: $dockerfile"
    echo "  Tag:        $tag"

    if [[ ! -f "$dockerfile_path" ]]; then
        echo -e "  ${RED}✗ Dockerfile not found${NC}"
        ((FAIL++))
        echo ""
        continue
    fi

    if [[ "$DRY_RUN" == true ]]; then
        echo -e "  ${YELLOW}⚠ Dry run - skipping build${NC}"
        ((SKIP++))
        echo ""
        continue
    fi

    # Build the image
    if [[ "$VERBOSE" == true ]]; then
        if docker build -t "$tag" -f "$dockerfile_path" "$context_path"; then
            echo -e "  ${GREEN}✓ Build successful${NC}"
            ((PASS++))
        else
            echo -e "  ${RED}✗ Build failed${NC}"
            ((FAIL++))
        fi
    else
        if docker build -t "$tag" -f "$dockerfile_path" "$context_path" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓ Build successful${NC}"
            ((PASS++))
        else
            echo -e "  ${RED}✗ Build failed (run with --verbose for details)${NC}"
            ((FAIL++))
        fi
    fi

    echo ""
done

# Summary
echo "========================================"
echo "  Build Summary"
echo "========================================"
echo ""
echo -e "Passed:  ${GREEN}$PASS${NC}"
echo -e "Failed:  ${RED}$FAIL${NC}"
echo -e "Skipped: ${YELLOW}$SKIP${NC}"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo -e "${RED}Some builds failed${NC}"
    exit 1
else
    echo -e "${GREEN}All builds passed${NC}"
    exit 0
fi
