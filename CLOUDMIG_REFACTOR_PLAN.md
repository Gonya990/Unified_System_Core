# Roadmap: Unified System Core - Cloud Automation & GitHub Models

## Project Objective / Цель проекта

Transform the current manual bot operations into a fully automated, scalable,
and resilient cloud infrastructure (GKE) integrated with GitHub Enterprise and
GitHub Models.

Превратить текущую ручную эксплуатацию ботов в полностью автоматизированную,
масштабируемую и отказоустойчивую облачную инфраструктуру (GKE),
интегрированную с GitHub Enterprise и GitHub Models.

---

## Phase 1: GKE Automation (Vibranium Cloud) / Фаза 1: Автоматизация GKE

**Goal:** Zero-manual-deployment. All changes go to the cloud automatically.
**Цель:** Нулевое ручное вмешательство. Все изменения попадают в облако автоматически.

1. **Artifact Registry Setup / Настройка Artifact Registry:**
    * Create a secure Docker registry in GCP.
    * Создать защищенный Docker-реестр в GCP.
2. **GitHub Actions CI Pipeline / Конвейер CI в GitHub Actions:**
    * Auto-build Docker image on every push to `main`.
    * Auto-push to Artifact Registry.
    * Автоматическая сборка Docker-образа при пуше в `main`.
    * Автоматический пуш в Artifact Registry.
3. **Secret Manager Integration / Интеграция Secret Manager:**
    * Migrate all keys (ByBit, Telegram, AI) from `.env` to GCP Secret Manager.
    * Refactor bot to fetch secrets via IAM Service Account.
    * Перенести все ключи из `.env` в GCP Secret Manager.
    * Рефакторинг бота для получения секретов через IAM Service Account.
4. **ArgoCD (GitOps) Deployment / Развертывание через ArgoCD:**
    * Install ArgoCD in the Kubernetes cluster.
    * Link to the `/k8s` folder in GitHub for automatic "Pull" deployment.
    * Установить ArgoCD в кластер Kubernetes.
    * Связать с папкой `/k8s` в GitHub для автоматического деплоя.

---

## Phase 2: GitHub Enterprise & Models / Фаза 2: GitHub Enterprise и Модели

**Goal:** State-of-the-art developer environment and AI redundancy.
**Цель:** Передовая среда разработки и резервирование AI.

1. **Workload Identity Federation / Федерация удостоверений:**
    * Connect GitHub Actions to GCP without long-lived keys.
    * Связать GitHub Actions с GCP без использования долгоживущих ключей.
2. **GitHub Models Provider / Провайдер GitHub Models:**
    * Add GitHub Models (Llama 3, Phi-3, Claude) as a new AI backend in the bot.
    * Implement auto-failover (if Gemini is down -> use GitHub Models).
    * Добавить GitHub Models как новый бэкенд AI в боте.
    * Реализовать авто-переключение (если Gemini лежит -> использовать GitHub Models).
3. **Automated Self-Healing / Автоматическое восстановление:**
    * If a Pod fails in GKE, the bot reports the log to GitHub Issue automatically.
    * The Agent (Me) analyzes the Issue using GitHub Models and prepares a fix.
    * Если Под в GKE падает, бот сам создает Issue в GitHub с логами.
    * Агент (Я) анализирует Issue через GitHub Models и готовит фикс.

---

## Execution Checklist / Чек-лист выполнения

* [x] Create Artifact Registry Repository (**Done**)
* [x] Create `.github/workflows/deploy.yaml` (**Done**)
* [x] Register GitHub Models API in the bot logic (**Done**)
* [ ] Provision GCP Secret Manager secrets
* [ ] Update GKE Deployment manifests to bind Secrets
