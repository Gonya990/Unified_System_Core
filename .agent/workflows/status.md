---
description: Check system status across all nodes
---
1. Check Tailscale connectivity:

```bash
tailscale status
```

1. Ping primary nodes (excluding rocinante - deprecated):

```bash
# pve-antigravity-1 | igor-gaming | smart | unified-home-core-cloud
ping -c 2 100.74.137.122 && ping -c 2 100.127.194.111 && ping -c 2 100.81.133.25 && ping -c 2 100.110.209.49
```

1. Check git status:

```bash
git status --short
```
