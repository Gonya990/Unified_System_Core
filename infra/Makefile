# Unified System Core - Deployment Makefile
# Common deployment and validation tasks

.PHONY: help validate test-builds lint-yaml lint-docker clean \
        build-all build-ai-bot build-mcp push-all \
        deploy-k8s deploy-compose up down logs

# Default target
help:
	@echo "Unified System Core - Deployment Commands"
	@echo ""
	@echo "Validation:"
	@echo "  make validate        Run all validation checks"
	@echo "  make lint-yaml       Lint YAML files"
	@echo "  make lint-docker     Lint Dockerfiles"
	@echo "  make test-builds     Test all Docker builds (dry-run)"
	@echo ""
	@echo "Building:"
	@echo "  make build-all       Build all Docker images"
	@echo "  make build-ai-bot    Build AI Telegram Bot image"
	@echo "  make build-mcp       Build all MCP server images"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-k8s      Deploy to Kubernetes (kustomize)"
	@echo "  make deploy-compose  Deploy with Docker Compose"
	@echo "  make up              Start services (compose)"
	@echo "  make down            Stop services (compose)"
	@echo "  make logs            Show logs (compose)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           Remove test images"

# =============================================================================
# Validation
# =============================================================================

validate:
	@./scripts/validate-manifests.sh

test-builds:
	@./scripts/test-docker-builds.sh --dry-run

lint-yaml:
	@echo "Linting YAML files..."
	@if command -v yamllint &> /dev/null; then \
		yamllint -d relaxed k8s/ docker-compose.unified.yml 2>/dev/null || true; \
	else \
		echo "yamllint not installed. Install with: pip install yamllint"; \
	fi

lint-docker:
	@echo "Linting Dockerfiles..."
	@if command -v hadolint &> /dev/null; then \
		find .. -name "Dockerfile*" -exec hadolint {} \; 2>/dev/null || true; \
	else \
		echo "hadolint not installed. Install from: https://github.com/hadolint/hadolint"; \
	fi

# =============================================================================
# Building
# =============================================================================

REGISTRY ?= ghcr.io/gonya990/unified_system_core
TAG ?= latest

build-all: build-ai-bot build-mcp build-web

build-ai-bot:
	@echo "Building AI Telegram Bot..."
	docker build -t $(REGISTRY)/ai-telegram-bot:$(TAG) \
		-f ../Projects/AI_Core/Dockerfile ../Projects/AI_Core

build-mcp: build-openai-mcp build-antigravity-mcp

build-openai-mcp:
	@echo "Building OpenAI MCP Gateway..."
	docker build -t $(REGISTRY)/openai-mcp-gateway:$(TAG) \
		-f ../Scripts/openai_mcp_server/Dockerfile ../Scripts/openai_mcp_server

build-antigravity-mcp:
	@echo "Building Antigravity MCP Server..."
	docker build -t $(REGISTRY)/antigravity-mcp:$(TAG) \
		-f ../Agent_Context/Knowledge_Base/mcp-server/Dockerfile \
		../Agent_Context/Knowledge_Base/mcp-server

build-web: build-chatkit build-connect

build-chatkit:
	@echo "Building ChatKit Dashboard..."
	docker build -t $(REGISTRY)/chatkit-dashboard:$(TAG) \
		-f ../Projects/ChatKit_Dashboard/Dockerfile ../Projects/ChatKit_Dashboard

build-connect:
	@echo "Building Connect Landing Page..."
	docker build -t $(REGISTRY)/connect-landing:$(TAG) \
		-f ../Projects/connect-landing-page/Dockerfile ../Projects/connect-landing-page

build-mail-processor:
	@echo "Building Mail Processor..."
	docker build -t $(REGISTRY)/mail-processor:$(TAG) \
		-f Dockerfile.mail-processor ..

# =============================================================================
# Push
# =============================================================================

push-all: push-ai-bot push-mcp push-web

push-ai-bot:
	docker push $(REGISTRY)/ai-telegram-bot:$(TAG)

push-mcp:
	docker push $(REGISTRY)/openai-mcp-gateway:$(TAG)
	docker push $(REGISTRY)/antigravity-mcp:$(TAG)

push-web:
	docker push $(REGISTRY)/chatkit-dashboard:$(TAG)
	docker push $(REGISTRY)/connect-landing:$(TAG)

# =============================================================================
# Deployment
# =============================================================================

deploy-k8s:
	@echo "Deploying to Kubernetes..."
	kubectl apply -k k8s/

deploy-ai-core-k8s:
	@echo "Deploying AI Core to Kubernetes..."
	kubectl apply -k ../Projects/AI_Core/k8s/

# Docker Compose deployment
COMPOSE_FILE ?= docker-compose.unified.yml
PROFILE ?= core

up:
	docker compose -f $(COMPOSE_FILE) --profile $(PROFILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) --profile $(PROFILE) down

logs:
	docker compose -f $(COMPOSE_FILE) --profile $(PROFILE) logs -f

ps:
	docker compose -f $(COMPOSE_FILE) --profile $(PROFILE) ps

restart:
	docker compose -f $(COMPOSE_FILE) --profile $(PROFILE) restart

# =============================================================================
# Maintenance
# =============================================================================

clean:
	@echo "Removing test images..."
	-docker rmi test-ai-bot:latest 2>/dev/null
	-docker rmi test-openai-mcp:latest 2>/dev/null
	-docker rmi test-antigravity-mcp:latest 2>/dev/null
	-docker rmi test-chatkit:latest 2>/dev/null
	-docker rmi test-connect:latest 2>/dev/null
	-docker rmi test-mail-processor:latest 2>/dev/null
	@echo "Done"

prune:
	@echo "Pruning Docker resources..."
	docker system prune -f
