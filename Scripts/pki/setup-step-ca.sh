#!/usr/bin/env bash
# Run on NUC as root or dedicated ca user
set -euo pipefail

CA_DIR="${CA_DIR:-/opt/unified/pki}"
PASSWORD_FILE="${CA_DIR}/.pass"

if ! command -v step >/dev/null 2>&1; then
  echo "Install step-cli: https://smallstep.com/docs/step-cli/" >&2
  exit 1
fi

mkdir -p "$CA_DIR"
export STEPPATH="$CA_DIR"

if [[ ! -f "$CA_DIR/config/ca.json" ]]; then
  echo "Initializing step-ca in $CA_DIR"
  step ca init \
    --deployment-type standalone \
    --name "Unified Core Root CA" \
    --dns "localhost,unified-ca.local" \
    --address ":8443" \
    --provisioner "admin@unified.local"
fi

echo "Start CA: step-ca --password-file $PASSWORD_FILE"
echo "For YubiKey-backed issuance, configure step-ca provisioner with attestation plugin (see docs/runbooks/pki-rotation.md)"
