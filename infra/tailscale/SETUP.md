# Tailscale GitOps Setup Instructions

## Prerequisites

- [x] Tailscale ACL file saved to `infra/tailscale/policy.jsonl`
- [x] GitHub Actions workflow created: `.github/workflows/tailscale-acl.yml`
- [ ] Tailscale API key generated
- [ ] GitHub secret configured

## Steps to Complete Setup

### 1. Generate Tailscale API Key

1. Visit <https://login.tailscale.com/admin/settings/keys>
2. Click **Generate API key**
3. **Scopes:** Select `Read & Write` for ACLs
4. **Description:** `GitHub Actions - ACL Sync`
5. Copy the generated key (format: `tskey-api-xxxxxxxxxx`)

### 2. Add GitHub Secret

1. Go to <https://github.com/Unified-system-Core/Unified_System_Core/settings/secrets/actions>
2. Click **New repository secret**
3. **Name:** `TAILSCALE_API_KEY`
4. **Value:** Paste the API key from step 1
5. Click **Add secret**

### 3. Test Deployment

```bash
# Make a test change to the ACL
echo "// Test GitOps deployment" >> infra/tailscale/policy.jsonl
git add infra/tailscale/policy.jsonl
git commit -m "test: GitOps ACL deployment"
git push origin main
```

### 4. Verify

1. Check GitHub Actions: <https://github.com/Unified-system-Core/Unified_System_Core/actions>
2. Verify ACL updated: <https://login.tailscale.com/admin/acls>
3. Check for the test comment in the live ACL

### 5. Cleanup Test

```bash
# Remove test comment
git revert HEAD
git push origin main
```

## Troubleshooting

**Workflow fails with "401 Unauthorized":**

- Check that `TAILSCALE_API_KEY` secret is set correctly
- Verify API key has ACL write permissions

**Workflow fails validation:**

- Run locally: `tailscale configure acl validate infra/tailscale/policy.jsonl`
- Fix syntax errors in the policy file

**Changes don't apply:**

- Ensure you pushed to `main` branch
- Check that file path is exactly `infra/tailscale/policy.jsonl`

## Next Steps

After successful setup:

- ✅ All ACL changes go through Git
- ✅ Automatic validation before deployment
- ✅ Full audit trail in Git history
- ✅ Easy rollback with `git revert`
