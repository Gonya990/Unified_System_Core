# Service Port Allocations

| Service | Port | Description |
|---------|------|-------------|
| **AI Telegram Bot** | `8080`, `8443` | Webhook & Health Check |
| **Content Factory** | `8095` | API & Workers |
| **Two Chimps** | `8090` | Video Gen Services |
| **Cliproxy API** | `8000` | LLM Gateway |
| **Grafana** | `3000` | Monitoring Dashboards |
| **Prometheus** | `9090` | Metrics Collection |
| **RabbitMQ** | `5672`, `15672` | Task Queue & UI |
| **Redis** | `6379` | Cache |
| **PostgreSQL** | `5432` | Primary DB |

> **Note:** New services should request ports in the `8100-8199` range.
