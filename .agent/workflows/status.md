---
description: Check system status across all nodes
---
1. Check Tailscale connectivity:

```bash
tailscale status
```

2. Ping primary nodes (excluding rocinante - deprecated):

```bash
ping -c 2 100.88.65.71 && ping -c 2 100.127.194.111 && ping -c 2 100.74.194.25 && ping -c 2 100.110.209.49
```

3. Check git status:

```bash
git status --short
```
