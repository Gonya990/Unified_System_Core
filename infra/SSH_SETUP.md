# SSH Access Setup: code-minion Server

## Current Status

### Existing Configuration
- **SSH Config Entry**: ✓ Configured in `~/.ssh/config`
- **Private Key**: ✓ Exists at `~/.ssh/kosta-code-minion` (600 permissions)
- **Public Key**: ✓ Exists at `~/.ssh/kosta-code-minion.pub`
- **Server Address**: `code-minion` (100.100.134.4)
- **Remote User**: `gonya`

### Issue
SSH authentication currently fails with `Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`.

**Root Cause**: The public key has not been added to `~/.ssh/authorized_keys` on the code-minion server.

---

## SSH Key Details

### Public Key
```
Location: ~/.ssh/kosta-code-minion.pub
Type: ssh-ed25519
Content:
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBngA8iPTGf9NlCBVCg1FqRKUencZ3zAXVVlDQt6RLOg igor-key
```

### SSH Config (already set up)
```
Host code-minion
    HostName 100.100.134.4
    User gonya
    IdentityFile ~/.ssh/kosta-code-minion
    StrictHostKeyChecking no
```

---

## Setup Instructions for Server Administrator

To enable SSH access to code-minion server (100.100.134.4):

### Option 1: Add Public Key to authorized_keys (Recommended)

1. **Login to code-minion** (using existing credentials or physical access):
   ```bash
   ssh gonya@100.100.134.4
   # or
   ssh -i /path/to/existing/key code-minion
   ```

2. **Add the public key to authorized_keys**:
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh

   # Paste the public key content below into authorized_keys:
   cat >> ~/.ssh/authorized_keys << 'EOF'
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBngA8iPTGf9NlCBVCg1FqRKUencZ3zAXVVlDQt6RLOg igor-key
   EOF

   chmod 600 ~/.ssh/authorized_keys
   ```

3. **Verify**:
   ```bash
   ls -la ~/.ssh/authorized_keys
   # Output should show: -rw------- 1 gonya gonya ... ~/.ssh/authorized_keys
   ```

### Option 2: Automated Setup (If SSH Admin Access Available)

If you have administrative access to the server, run:
```bash
ssh gonya@100.100.134.4 << 'SETUP'
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBngA8iPTGf9NlCBVCg1FqRKUencZ3zAXVVlDQt6RLOg igor-key' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
SETUP
```

---

## Verification After Setup

Once the public key is added to the server, test SSH access from macbook:

```bash
# Test SSH connection
ssh code-minion "whoami"

# Expected output:
# gonya

# Or full login
ssh code-minion

# Check server system info
ssh code-minion "uname -a"
```

---

## Troubleshooting

### If SSH still fails after adding key:

1. **Verify SSH service is running on server**:
   ```bash
   ssh code-minion "sudo systemctl status ssh"
   ```

2. **Check permissions on server**:
   ```bash
   ssh code-minion "ls -la ~/.ssh/"
   # Should show:
   # drwx------ ... ~/.ssh
   # -rw------- ... ~/.ssh/authorized_keys
   ```

3. **Verify public key format**:
   ```bash
   ssh-keygen -l -f ~/.ssh/kosta-code-minion.pub
   # Should show fingerprint for key type ED25519
   ```

4. **Enable SSH verbose logging**:
   ```bash
   ssh -vvv code-minion "whoami"
   # Look for "Authentications that can continue: publickey"
   ```

5. **Check /var/log/auth.log on server** (if you have access):
   ```bash
   ssh code-minion "tail -20 /var/log/auth.log | grep -i ssh"
   ```

---

## Security Notes

- Private key (`kosta-code-minion`) has restricted permissions (600)
- Public key can be safely shared and added to multiple systems
- `StrictHostKeyChecking no` is configured for non-interactive access
  - Set to `yes` if you need host key verification after initial setup
  - Current setting: permissive (suitable for internal infrastructure)

---

## Next Steps

1. Server admin adds public key to `~/.ssh/authorized_keys` on code-minion
2. Test SSH connection: `ssh code-minion "whoami"`
3. Use for remote operations (e.g., deployment, monitoring, CI/CD)

---

## Related Issues

- **US-6h6**: SSH access to code-minion server (this task)
- **OPS_RUNBOOK.md**: Server operations and management commands
