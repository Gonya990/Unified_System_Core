#!/bin/bash
# Script to automate Ubuntu Cloud Image deployment on Proxmox
# Requires: SSH access to Proxmox

PV_HOST="root@100.74.194.25"
VM_ID="106"
VM_NAME="unified-home-core-cloud"
STORAGE="nvme-thin"
PUB_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQClpxm27R7Q92+dbgG3ORcgF9xFzsH9gqfcg0/LQH9XLsWTYBwIgCuOkStUjGICQhgDq1n1wyb7ApK5CHYNMlO/E5rDZBVFaX381hPzS1H5rgpCyb0qKZbLIyReHyXJTTfFvNnwcg58IKFm63DF0TmPxCSoiG3egl4zdjuPehVVl7x8Niznl6kDbJQeg9lXrpXxGDHzVmFzVTK5QOz7xK+TeLLPixrBCLXcPcoClTBTNKGXaheWouysBKCXuf4419mu0w6HVOw+d4oL8PdeNepxbxnuWBSOvlGWHGE+wTK7N5rPeJWBqfY73AdgwG0ixagSDwRGgxNGt8uUmdv3l7YslngvD5jY19/J3cP5djU2guiooQq9RDvhJnr+cfzdrd5MUncfUEOSWl5v4h4IG+Dyd6FSfeussvu3/Ks23knzUs9zV2Gz1usMWDBPW2m9qfRa+ThQAj2Y9PoO0IwyPjanhXqKDaYL1Ye84FRLbmJ3iYUnL16GsPdYSjqidjI8DaI8HpmZa1ZenKQ4AZJvZIWqDRHfzpdxT4C+f4jIbCEK7fnC2QyeEfdvx1Eyal0t83N8oOlKnd/+LkNSbXi1yw4VMVa9wy9y8o0gFERyQMWtY9LMhPaFY7BLLKCtspt8YAphcS5i8t90sNOFnpzmX0lSp/a2BthlNOYxMzu6PSPEnQ== root@pve"

echo "Using Public Key: $PUB_KEY"

# Ensure old VM is gone
echo "Cleaning up old VM $VM_ID..."
ssh -o StrictHostKeyChecking=no $PV_HOST "qm stop $VM_ID || true; qm destroy $VM_ID || true"

# Download Image
echo "Checking/Downloading Ubuntu Cloud Image..."
ssh -o StrictHostKeyChecking=no $PV_HOST "
if [ ! -f /var/lib/vz/template/iso/ubuntu-22.04-server-cloudimg-amd64.img ]; then
    wget -O /var/lib/vz/template/iso/ubuntu-22.04-server-cloudimg-amd64.img https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
fi
"

# Create VM
echo "Creating VM $VM_ID..."
# Steps:
# 1. Create VM
# 2. Import disk
# 3. Attach disk
# 4. Set Cloud-Init
# 5. Set user/keys
ssh -o StrictHostKeyChecking=no $PV_HOST "
qm create $VM_ID --name $VM_NAME --memory 4096 --cores 2 --net0 virtio,bridge=vmbr0
qm importdisk $VM_ID /var/lib/vz/template/iso/ubuntu-22.04-server-cloudimg-amd64.img $STORAGE
qm set $VM_ID --scsihw virtio-scsi-pci --scsi0 $STORAGE:vm-$VM_ID-disk-0
qm set $VM_ID --ide2 $STORAGE:cloudinit
qm set $VM_ID --boot c --bootdisk scsi0
qm set $VM_ID --serial0 socket --vga serial0
qm set $VM_ID --ipconfig0 ip=dhcp
qm set $VM_ID --sshkey <(echo \"$PUB_KEY\")
qm set $VM_ID --ciuser gonya
qm resize $VM_ID scsi0 +32G
qm start $VM_ID
"

echo "VM $VM_ID started! Waiting for it to boot..."
