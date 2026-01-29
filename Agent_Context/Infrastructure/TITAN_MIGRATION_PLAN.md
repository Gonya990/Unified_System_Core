# 🏗️ План Миграции на TITAN (Proxmox Cluster)

**Цель:** Перенос вычислительных мощностей Unified System на выделенный
сервер Proxmox (IP: `100.78.145.67`).

## 1. Архитектура Контейнеров (LXC)

Мы разделим монолитную систему на изолированные микросервисы (LXC контейнеры)
для максимальной надежности и управляемости.

| ID | Hostname | Role | Resources |
|----|----------|------|-----------|
| **101** | `us-core-bot-igor` | Igor's Bot | 2 CPU, 2GB |
| **102** | `us-core-bot-kostya` | Kostya's Bot | 2 CPU, 2GB |
| **103** | `us-mcp-mail` | MCP Server | 2 CPU, 4GB |
| **104** | `us-content-factory` | Content Factory | 4 CPU, 8GB |
| **105** | `us-db-redis` | DB (Pg/Redis) | 2 CPU, 4GB |

## 2. Инструкция для Infrastructure Admin (Kostya)

Так как у нас нет API токена, **Костя должен выполнить следующие действия на Титане:**

### A. Подготовка шаблона

Убедитесь, что шаблон `ubuntu-22.04-standard` доступен в хранилище `local`.

```bash
pveam update
pveam download local ubuntu-22.04-standard_22.04-1_amd64.tar.zst
```

### B. Создание Контейнеров (Скрипт)

Сохраните этот скрипт как `create_unified_cluster.sh` на Титане и запустите:

```bash
#!/bin/bash
# Создание кластера Unified System

# 1. Igor's Bot
pct create 101 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname us-core-bot-igor --cores 2 --memory 2048 --swap 512 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp --features nesting=1 \
  --password "TemporaryPassword123!" \
  --ssh-public-keys /root/.ssh/authorized_keys

# 2. Kostya's Bot
pct create 102 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname us-core-bot-kostya --cores 2 --memory 2048 --swap 512 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp --features nesting=1 \
  --password "TemporaryPassword123!" \
  --ssh-public-keys /root/.ssh/authorized_keys

# 3. Start Containers
pct start 101
pct start 102

echo "✅ Containers created. Please install Tailscale inside each container."
```

## 3. Настройка Сети (Tailscale в LXC)

После запуска контейнеров, в **каждом** из них нужно:

1. Установить Tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Авторизовать: `tailscale up --authkey <AUTH_KEY>`

## 4. Развертывание Кода

Как только контейнеры появятся в сети Tailscale (получат IP 100.x.x.x),
мы запустим наш скрипт `deploy_to_core.sh`, изменив целевой IP на IP новых контейнеров.

---
**Authored by:** Antigravity Agent
**Date:** 2026-01-15
