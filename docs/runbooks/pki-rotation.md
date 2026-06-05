# PKI rotation — Unified Root CA (NUC)

## Topology

- **Root CA**: `step-ca` on NUC Linux (recommended OpenClaw host).
- **YubiKey PIV**: required to sign new device certificates (not left plugged in 24/7).
- **Tailscale**: mesh transport; mTLS is additional app-layer trust.

## Initial setup

```bash
# On NUC
./scripts/pki/setup-step-ca.sh
```

## Issue client certificate

```bash
./scripts/pki/issue-client-cert.sh --name macbook-air --san 100.68.240.51
./scripts/pki/issue-client-cert.sh --name igor-gaming --san igor-gaming.ayu-altair.ts.net
```

## iPhone profiles

Export `.mobileconfig` from step-ca or install PEM via Apple Configurator.

## Rotation

1. Generate new intermediate (annual).
2. Re-issue service certs with 90-day TTL.
3. Update `SYSTEM_MAP.md` fingerprint table.
4. Revoke compromised certs in `step-ca` DB.

## Telegram app-layer keys

After device certs work, generate NaCl keypair:

```bash
python3 -c "from lib.telegram_crypto import generate_keypair; import base64; sk,pk=generate_keypair(); print('PRIV', base64.b64encode(sk).decode()); print('PUB', base64.b64encode(pk).decode())"
```

Store in TokenBroker; never commit.
