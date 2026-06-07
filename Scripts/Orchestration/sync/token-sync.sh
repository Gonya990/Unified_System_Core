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
    "gpu-node-1"
    "igor-gaming"
)

echo -e "${GREEN}🔐 Token Sync Started${NC}"

if [ ! -f "$VAULT_PATH" ]; then
    echo -e "${RED}✗ Local vault not found at $VAULT_PATH${NC}"
    exit 1
fi

for NODE in "${NODES[@]}"; do
    echo -e "${YELLOW}>>> Syncing vault to $NODE...${NC}"
    
    # Check connectivity with timeout first
    if ! ssh -q -o BatchMode=yes -o ConnectTimeout=5 "$NODE" exit; then
        echo -e "${RED}✗ Cannot connect to $NODE. Skipping.${NC}"
        continue
    fi
    
    if [ "$NODE" = "igor-gaming" ]; then
        # Ensure WSL config directory exists
        ssh -o ConnectTimeout=5 "$NODE" "wsl mkdir -p /home/gonya/.config/unified-system"
        # Sync via wsl tee to write directly to WSL filesystem
        if ssh -o ConnectTimeout=5 "$NODE" "wsl tee /home/gonya/.config/unified-system/tokens.yaml > /dev/null" < "$VAULT_PATH"; then
            echo -e "${GREEN}✓ Vault successfully synced to $NODE (WSL).${NC}"
        else
            echo -e "${RED}✗ Failed to sync vault to $NODE (WSL).${NC}"
        fi
    else
        # Ensure remote directory exists
        ssh -o ConnectTimeout=5 "$NODE" "mkdir -p ~/.config/unified-system"
        # Securely copy the vault
        if scp -o ConnectTimeout=5 -p "$VAULT_PATH" "$NODE:~/.config/unified-system/tokens.yaml"; then
            echo -e "${GREEN}✓ Vault successfully synced to $NODE.${NC}"
        else
            echo -e "${RED}✗ Failed to sync vault to $NODE. Check SSH/Tailscale.${NC}"
        fi
    fi
done

echo -e "${GREEN}✓ Token synchronization complete.${NC}"
