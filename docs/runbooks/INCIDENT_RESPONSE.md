# 🚨 Incident Response Runbook

This document outlines the standard procedure for handling production incidents in the **Unified System Core**.

## 1. Detection & Classification

**Triggers:**

* **GCP Alert**: Notification in Telegram/Email (High Severity).
* **User Report**: Direct message to `@gonya_bot` or linear ticket.
* **Health Check Failure**: `/health` endpoint returning 500.

**Severity Levels:**

| Level | Description | Example | Response SLA |
| :--- | :--- | :--- | :--- |
| **SEV-1 (Critical)** | Core service down (Bot, Trading). Data loss risk. | Bot stopped responding. Trade execution failed. | **15 mins** |
| **SEV-2 (High)** | Major feature broken. Workaround exists. | Voice messages not working. Image gen slow. | **1 hour** |
| **SEV-3 (Medium)** | Minor bug, cosmetic issue. | Typo in response. Slow dashboard load. | **24 hours** |
| **SEV-4 (Low)** | Request for enhancement / minor annoyance. | Lint warning. | Next sprint |

## 2. Response Workflow (SEV-1/2)

1. **Acknowledge**:
    * Mark alert as "Ack" in Telegram/GCP.
    * Create Linear Issue: `[INCIDENT] <Title>`.

2. **Triage**:
    * Check Logs: `kubectl logs -l app=<service_name> -n default --tail=100`
    * Check Metrics: GCP Monitoring Dashboard.
    * Check Recent Changes: `git log -n 5` or recent deploy workflows.

3. **Mitigation (Stop the bleeding)**:
    * **Rollback**: `kubectl rollout undo deployment/<service_name>`
    * **Restart**: `kubectl rollout restart deployment/<service_name>`
    * **Scale Up**: `kubectl scale deployment/<service_name> --replicas=<N+1>`
    * **Disable Feature**: Turn off feature flag via ConfigMap/Env Var (`ENABLE_FEATURE_X=false`).

4. **Resolution**:
    * Identify root cause.
    * Develop fix on hotfix branch (`hotfix/inc-<id>`).
    * Deploy fix.

5. **Post-Mortem**:
    * Fill out `docs/post-mortems/template.md`.
    * Update runbooks/alerts to prevent recurrence.

## 3. Common Scenarios

### 🤖 Bot Not Responding

**Symptoms**: No reply to `/start`, webhook errors.
**Steps**:

1. Check Pod status: `kubectl get pods` (Look for CrashLoopBackOff).
2. Check Logs: `kubectl logs <pod_name>`.
3. Check Telegram API Status: Is Telegram down?
4. Restart Bot: `kubectl rollout restart deployment/ai-telegram-bot`.

### 📉 High Latency / OOM (Out of Memory)

**Symptoms**: Slow responses, random restarts.
**Steps**:

1. Check Memory Usage: `kubectl top pods`.
2. Check HPA Status: `kubectl get hpa`.
3. Increase Limits: Edit `deployment.yaml` limits/requests.

### 🔐 Secret Rotation Failure

**Symptoms**: Auth errors (401/403) to external APIs.
**Steps**:

1. Verify Secret version in GCP Secret Manager.
2. Verify ExternalSecret status: `kubectl get externalsecrets`.
3. Force sync: Delete the K8s secret to trigger re-sync (if using ExternalSecrets operator).
