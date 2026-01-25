# VASER-Hub Architecture Overview

## Purpose
VASER-Hub is the centralized execution and policy layer that brokers all
actions from the Super Admin GPT to managed devices, Home Assistant, local
Python gateways, and cloud services.

## Core Components
- **API Gateway**: Receives OpenAPI action requests and validates auth.
- **Policy Engine**: Enforces confirmation rules, risk classification, and
  deny/allow lists.
- **Credential Vault**: Stores SSH keys, API tokens, and endpoint metadata.
- **Execution Orchestrator**: Routes tasks to SSH/WinRM/API connectors.
- **Audit Logger**: Immutable event log and traceable action metadata.
- **Device Inventory**: Tracks devices, tags, states, and owner boundaries.

## Data Flow
1. GPT sends action request (OpenAPI).
2. API Gateway validates auth token.
3. Policy Engine evaluates risk and requires confirmation if needed.
4. Execution Orchestrator resolves device and executes via connector.
5. Results are returned and logged in Audit Logger.

## Execution Connectors
- **SSH**: Linux/Unix devices via jump hosts.
- **WinRM**: Windows hosts with constrained endpoints.
- **HTTP/API**: IoT and SaaS services.
- **Home Assistant**: Service calls and script execution.
- **Local Gateway**: /local/run, /local/read, /local/write operations.

## Security Boundaries
- VASER-Hub is isolated in a management subnet.
- Connectors operate with device-specific credentials.
- No direct access from GPT to devices; all traffic is mediated.

## Reliability & Resilience
- Queue-based execution with retries and timeouts.
- Safe rollback hooks for configuration changes.
- Circuit breakers for repeated failures.

## Observability
- Structured logs for each action.
- Metrics for latency, success rate, and error classification.
- Alerting hooks for high-risk activity.
