# Breaking Change Analysis: Firestore Health Check Failure

**Date**: 2026-01-15  
**Severity**: Critical  
**Status**: Resolved (rolled back)  
**Author**: Sisyphus Agent

---

## Summary

Uncommitted changes to `firestore_db.py` broke the GCP project ID resolution logic, causing Firestore health checks to fail and triggering "NO HEALTHY HEARTBEAT DETECTED" alerts.

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| ~04:00 | Autosave commits started accumulating changes |
| ~04:17 | `firestore_db.py` modified with broken logic |
| ~13:00 | Heartbeat failure detected |
| ~13:16 | Rollback executed |

---

## Root Cause

### The Bug

```python
# BEFORE (working):
proj_id = project_id or os.environ.get("GCP_PROJECT_ID", "my-home-435112")

# AFTER (broken):
proj_id = os.environ.get("GCP_PROJECT_ID", project_id)
```

### Why It Breaks

| Scenario | OLD Behavior | NEW Behavior |
|----------|--------------|--------------|
| `project_id=None`, env unset | `"my-home-435112"` | `None` |
| `project_id="foo"`, env unset | `"foo"` | `None` (then `"foo"` as default) |
| `project_id=None`, env=`"bar"` | `"bar"` | `"bar"` |

The new logic uses `project_id` as the *default* for `os.environ.get()`, not as a primary value. When both are `None`, the result is `None`, causing Firestore client initialization to fail.

### Secondary Issues

1. **Credential Mismatch**: `gcp-service-account.json` was swapped to `ivory-cycle-484403-i4` but code still defaulted to `my-home-435112`
2. **Duplicate Env Var**: `docker-compose.yml` had duplicate `GCP_PROJECT_ID` lines
3. **health_check() Changed**: Query target changed from `_health.check` to `users.limit(1).stream()`

---

## Impact

- Firestore client failed to initialize (project=None)
- Health check endpoint returned errors
- Watchdog detected consecutive failures
- System reported unhealthy state

---

## Resolution

Rolled back three files to last known good state:

```bash
git checkout -- \
  Projects/AI_Core/src/firestore_db.py \
  Projects/AI_Core/docker-compose.yml \
  Projects/AI_Core/gcp-service-account.json
```

---

## Prevention Measures

### Immediate

1. **Pre-commit Hook**: Add Firestore connectivity test before allowing commits to `firestore_db.py`
2. **Atomic Credential Updates**: Credential + code changes must be in same commit

### Recommended

| Control | Implementation |
|---------|----------------|
| **Config Validation** | Add startup check that validates `proj_id is not None` |
| **Health Check Isolation** | Health check should not depend on specific collections existing |
| **Change Detection** | Alert on uncommitted changes to critical files after N hours |

### Code Fix (if migration proceeds)

```python
# Correct pattern for optional param with env override:
proj_id = os.environ.get("GCP_PROJECT_ID") or project_id or "my-home-435112"
```

Or explicitly:

```python
proj_id = os.environ.get("GCP_PROJECT_ID")
if not proj_id:
    proj_id = project_id if project_id else "my-home-435112"
```

---

## Files Affected

| File | Change Type | Rolled Back |
|------|-------------|-------------|
| `Projects/AI_Core/src/firestore_db.py` | Logic bug | Yes |
| `Projects/AI_Core/docker-compose.yml` | Duplicate env | Yes |
| `Projects/AI_Core/gcp-service-account.json` | Credential swap | Yes |
| `Projects/AI_Core/src/agent_mail_client.py` | SDK paths (non-breaking) | No |

---

## Lessons Learned

1. **Python `or` vs `dict.get()` default**: These have different semantics. `a or b` returns first truthy value. `dict.get(key, default)` returns default only if key is missing, not if value is falsy.

2. **Uncommitted != Safe**: Autosave can accumulate breaking changes in working directory without triggering CI.

3. **Credential migrations are atomic**: Never change credentials without ensuring code can use them.

---

## Related Issues

- US-xyz: Add pre-commit Firestore validation (TODO: create)
- US-abc: Implement config startup validation (TODO: create)
