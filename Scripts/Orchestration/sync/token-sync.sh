#!/bash
# Token Sync - Synchronizes the secure Vibranium vault across nodes
# Logic: Local Vault -> Remote Nodes

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

VAULT_PATH="$HOME/.config/unified-system/tokens.yaml"
NODES=(
    "unified-home-core-cloud"
    "gpu-node-1"
)

echo -e "${GREEN}🔐 Token Sync Started${NC}"

if [ ! -f "$VAULT_PATH" ]; then
    echo -e "${RED}✗ Local vault not found at $VAULT_PATH${NC}"
    exit 1
fi

for NODE in "${NODES[@]}"; do
    echo -e "${YELLOW}>>> Syncing vault to $NODE...${NC}"
    
    # Ensure remote directory exists
    ssh "$NODE" "mkdir -p ~/.config/unified-system"
    
    # Securely copy the vault
    if scp -p "$VAULT_PATH" "$NODE:~/.config/unified-system/tokens.yaml"; then
        echo -e "${GREEN}✓ Vault successfully synced to $NODE.${NC}"
    else
        echo -e "${RED}✗ Failed to sync vault to $NODE. Check SSH/Tailscale.${NC}"
    fi
done

echo -e "${GREEN}✓ Token synchronization complete.${NC}"
