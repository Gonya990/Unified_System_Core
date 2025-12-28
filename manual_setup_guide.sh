#!/bin/bash
# Interactive Manual Setup Guide for Igor-Gaming-1

echo "============================================="
echo "   🚀 GUIDE: MANUAL SETUP & TROUBLESHOOTING"
echo "============================================="
echo ""
echo "This script will help you complete the tasks:"
echo "1. Deploy Budget Alert Fix (GCP)"
echo "2. Setup SSH for Distributed AI (PVE)"
echo ""

# --- Step 1: GCP Deployment ---
echo "--- Step 1: Fixed Budget Alert Deployment ---"
echo "Attempting to deploy from correct path..."
echo ""
read -p "Press Enter to run deployment command..."

echo "Deleting conflicting Gen 2 function if exists..."
gcloud functions delete budget_alert_telegram --region=us-central1 --quiet || echo "Function did not exist or delete failed (continuing)"

DEPLOY_CMD="gcloud functions deploy budget_alert_telegram \
  --runtime python311 \
  --trigger-topic budget-alerts \
  --entry-point budget_alert_telegram \
  --no-gen2 \
  --source Unified_System/cloud_functions/budget_alert_telegram"

echo "Running: $DEPLOY_CMD"
$DEPLOY_CMD

if [ $? -eq 0 ]; then
    echo "✅ Deployment Successful!"
else
    echo "❌ Deployment Failed. Please check the error above."
fi

echo ""
echo "---------------------------------------------"
echo ""

# --- Step 2: SSH Setup ---
echo "--- Step 2: SSH Setup for Distributed AI ---"
echo "If the automated script failed, we must do this manually."
echo ""
echo "Please execute the following command MANUALLY on this server:"
echo ""
echo "   ssh-copy-id root@100.74.137.122"
echo ""
echo "Tip: Try passwords 'GarYk6550', 'Gonya990', '6550' or look for 'Proxmox Root Password' in your notes."
echo "" 
read -p "Did you succeed? (y/n): " ssh_success

if [ "$ssh_success" == "y" ]; then
    echo "✅ Great! Distributed AI is ready."
else
    echo "⚠️  No worries. We can try resetting the PVE root password later via Proxmox web UI."
fi

echo ""
echo "============================================="
echo "   🎉 GUIDE COMPLETE"
echo "============================================="
