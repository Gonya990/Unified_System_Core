#!/bin/bash
# Build Bot Local - Build and Load K8s Image on Single Node (unified-home-core-cloud)
# Usage: ./build-bot-local.sh

set -euo pipefail

# Check if we are on the correct node (can be run via SSH too)
if [[ "$(hostname)" != "unified-home-core-cloud" ]]; then
    # If not on the node, SSH and execute itself (assuming file is synced)
    # But files are synced to /home/gonya/Unified_System/Scripts/...
    echo "Remote execution on unified-home-core-cloud..."
    ssh unified-home-core-cloud "bash /home/gonya/Unified_System/Scripts/Orchestration/deploy/build-bot-local.sh"
    exit $?
fi

echo "💎 Building Local AI Bot Image for K3s..."
cd /home/gonya/Unified_System

# 1. Build the image using Docker (or BuildKit directly if available, but Docker is standard)
# We use the tag expected by the deployment: ai-telegram-bot:local
if sudo docker build -t ai-telegram-bot:local -f Projects/AI_Core/Dockerfile .; then
    echo "✓ Docker build successful."
else
    echo "✗ Docker build failed."
    exit 1
fi

# 2. Import into K3s (containerd)
echo "Importing into K3s registry..."
# Save to tar and pipe to k3s ctr
# Note: k3s uses containerd. 'k3s ctr images import' handles .tar archives.
# 'docker save' produces a tar.
if sudo docker save ai-telegram-bot:local | sudo k3s ctr images import -; then
    echo "✓ Image imported into K3s."
else
    echo "✗ Failed to import image into K3s."
    exit 1
fi

# 3. Restart Deployment to pick up new image (since Policy is IfNotPresent, we might need to delete pod or rely on hash change if we used a unique tag)
# But since we overwrote 'ai-telegram-bot:local', we need to force a pull or just kill the pod.
# However, IfNotPresent + same tag = no pull.
# We should probably delete the old image from k3s first?
# "sudo k3s ctr images remove docker.io/library/ai-telegram-bot:local"
# But importing overwrites usually.

echo "Restarting deployment..."
sudo kubectl rollout restart deployment/ai-telegram-bot -n trading

echo "✓ Bot update sequence complete."
