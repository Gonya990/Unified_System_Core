# Resolve Connectivity and Host Entries

The user is experiencing connection issues between their Mac and Linux machine, likely due to outdated or commented-out host entries. We will update the Mac's `/etc/hosts` file to use Tailscale IPs for reliable access to local services.

## User Review Required

> [!IMPORTANT]
> This plan requires the user to manually edit the `/etc/hosts` file on their **MacBook Air**, as I do not have direct access to that machine.

## Proposed Changes

### Mac OS Configuration

#### [MODIFY] Mac `/etc/hosts`

Update the hosts file on the Mac to include the Tailscale IP of the Linux machine (`igor-gaming-1`).

Proposed entry:

```bash
100.88.65.71 mydomain.com
```

### Linux Machine (igor-gaming-1)

No changes required, but we will use the following services for verification:

- **Home Assistant**: `http://mydomain.com:8123`
- **n8n**: `http://mydomain.com:8080` (or `5678`)
- **Ollama**: `http://mydomain.com:11434`

## Verification Plan

### Manual Verification

1. On the **MacBook Air**, run:

   ```bash
   ping mydomain.com
   ```

   Confirm it resolves to `100.88.65.71`.
2. Open the following URLs in the Mac's browser:
   - `http://mydomain.com:8123`
   - `http://mydomain.com:11434/api/tags`
3. Verify that the browser no longer shows `chrome-error://chromewebdata/`.
