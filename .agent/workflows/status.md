---
description: Check system status across all nodes
---
# 📊 System Status Check

1. Check Tailscale connectivity:

```bash
tailscale status
```

1. Ping primary nodes (excluding rocinante - deprecated):

```bash
# gpu-node-1 | igor-gaming-1 | smart | unified-home-core-cloud
ping -c 2 100.67.107.71 && ping -c 2 100.115.17.68 && \
ping -c 2 100.118.179.47 && ping -c 2 100.87.208.56
```

1. Check git status:

```bash
git status --short
```
