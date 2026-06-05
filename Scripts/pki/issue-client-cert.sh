#!/usr/bin/env bash
set -euo pipefail

NAME=""
SAN=""
CA_URL="${CA_URL:-https://localhost:8443}"

usage() {
  echo "Usage: $0 --name <client> --san <dns-or-ip>" >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) NAME="$2"; shift 2 ;;
    --san) SAN="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[[ -n "$NAME" && -n "$SAN" ]] || usage

OUT_DIR="/opt/unified/pki/clients/${NAME}"
mkdir -p "$OUT_DIR"

step ca certificate "${NAME}.crt" "${OUT_DIR}/${NAME}.csr" \
  --san "$SAN" \
  --ca-url "$CA_URL" \
  --provisioner "admin@unified.local"

echo "Issued: $OUT_DIR/${NAME}.crt"
