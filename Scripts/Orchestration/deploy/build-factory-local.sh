#!/bin/bash
# Build Factory Local - Build and Load Factory Image
# Usable for both single-node K3s (local) and development
# Usage: ./build-factory-local.sh

set -euo pipefail

# Check if we are on the correct node (can be run via SSH too)
if [[ "$(hostname)" != "unified-home-core-cloud" ]]; then
    echo "Remote execution on unified-home-core-cloud..."
    ssh unified-home-core-cloud "bash /home/gonya/Unified_System/Scripts/Orchestration/deploy/build-factory-local.sh"
    exit $?
fi

echo "💎 Building Local Content Factory Image for K3s..."
cd /home/gonya/Unified_System/Projects/Content_Factory

# 1. Build the image using Docker
if sudo docker build -t content-factory:local .; then
    echo "✓ Docker build successful."
else
    echo "✗ Docker build failed."
    exit 1
fi

# 2. Import into K3s (containerd)
echo "Importing into K3s registry..."
if sudo docker save content-factory:local | sudo k3s ctr images import -; then
    echo "✓ Image imported into K3s."
else
    echo "✗ Failed to import image into K3s."
    exit 1
fi

# 3. Clean up evicted pods
echo "Cleaning up evicted pods..."
sudo kubectl delete pods --field-selector=status.phase=Failed -n factory || true

# 4. Apply updated manifest (should be uploaded before running this, or we rely on vibranium-sync)
# Assuming manifest is at Projects/Content_Factory/k8s/factory_all_in_one.yaml (relative to root)
cd /home/gonya/Unified_System
if [ -f Projects/Content_Factory/k8s/factory_all_in_one.yaml ]; then
    echo "Applying K8s manifest..."
    sudo kubectl apply -f Projects/Content_Factory/k8s/factory_all_in_one.yaml
    echo "✓ Manifest applied."
else
    echo "⚠ Manifest not found, skipping apply step."
fi

# Restart daemonset/deployment if needed (actually it's a CronJob, so next run will pick it up, but there is also a Deployment 'content-factory-orchestrator')
echo "Restarting deployment..."
sudo kubectl rollout restart deployment/content-factory-orchestrator -n factory || true

echo "✓ Factory update sequence complete."
