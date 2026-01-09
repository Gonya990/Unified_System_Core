# CLIProxyAPI Infrastructure

Centralized proxy and authentication management for AI services.

## Architecture

- **Primary Service**: `cliproxyapi` (Writer)
  - Handles authentication, key rotation, and proxying requests.
  - Stores credentials in `./auth_db` (mapped to `/root/.cli-proxy-api`).
- **Auto-Update**: `watchtower`
  - Checks for updates to `eceasy/cli-proxy-api` every hour.
  - Automatically restarts the service with the new image.

## Directory Structure

```
infra/cliproxyapi/
├── docker-compose.yml  # Service definition
├── config.yaml         # App configuration
└── auth_db/            # Persisted auth storage (SQLite/JSON)
```

## Setup

1. **Network**: Ensure `centralized_net` exists:
   ```bash
   docker network create centralized_net || true
   ```

2. **Start**:
   ```bash
   docker-compose up -d
   ```

3. **Login**:
   Run the login command interactively on the running container:
   ```bash
   docker exec -it cliproxyapi ./CLIProxyAPI --login
   ```
   Follow the on-screen instructions to authenticate your accounts.

## Usage for Clients

Other services on the `centralized_net` network can access the proxy at:
`http://cliproxyapi:8317`

