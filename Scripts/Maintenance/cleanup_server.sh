#!/bin/bash
# Emergency disk cleanup for unified-home-core-cloud
# Run this as root on the server when disk is >90% full

set -e

echo "=== Starting emergency disk cleanup ==="

# 1. Clean journalctl logs (keep last 24 hours)
echo "[1/5] Cleaning system logs..."
journalctl --vacuum-time=1d
echo "✓ Logs cleaned"

# 2. Clean apt cache
echo "[2/5] Cleaning apt cache..."
apt-get clean
echo "✓ APT cache cleaned"

# 3. Docker cleanup (aggressive - removes all unused images/containers)
echo "[3/5] Cleaning Docker..."
docker system prune -af --volumes 2>/dev/null || echo "Docker not running or not installed"
echo "✓ Docker cleaned"

# 4. Remove temporary files
echo "[4/5] Cleaning /tmp and /var/tmp..."
rm -rf /tmp/* /var/tmp/* 2>/dev/null || true
echo "✓ Temp files cleaned"

# 5. Check final disk usage
echo "[5/5] Final disk status:"
df -h /

echo ""
echo "=== Cleanup complete! ==="
