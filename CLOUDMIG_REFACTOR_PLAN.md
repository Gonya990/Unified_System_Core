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
    * [x] Create a secure Docker registry in GCP (`unified-core-images`).
    * [x] Создать защищенный Docker-реестр в GCP (`unified-core-images`).
2. **GitHub Actions CI Pipeline / Конвейер CI в GitHub Actions:**
    * [x] Auto-build Docker image on every push to `main` (`.github/workflows/deploy.yaml`).
    * [x] Auto-push to Artifact Registry (`.github/workflows/deploy.yaml`).
    * [x] Автоматическая сборка Docker-образа при пуше в `main`.
    * [x] Автоматический пуш в Artifact Registry.
3. **Secret Manager Integration / Интеграция Secret Manager:**
    * [x] Migrate all keys (ByBit, Telegram, AI) from `.env` to GCP Secret Manager.
    * [x] Refactor bot to fetch secrets via IAM Service Account.
4. **ArgoCD (GitOps) Deployment / Развертывание через ArgoCD:**
    * [x] Install ArgoCD in the Kubernetes cluster.
    * [x] Link to the `/k8s` folder in GitHub for automatic "Pull" deployment.
    * [x] Configured Repository Secrets for private access.

---

## Phase 2: GitHub Enterprise & Models / Фаза 2: GitHub Enterprise и Модели

**Goal:** State-of-the-art developer environment and AI redundancy.
**Цель:** Передовая среда разработки и резервирование AI.

1. **Workload Identity Federation / Федерация удостоверений:**
    * [x] Connect GitHub Actions to GCP without long-lived keys (Pool: github-pool).
    * [x] Связать GitHub Actions с GCP без использования долгоживущих ключей.
2. **GitHub Models Provider / Провайдер GitHub Models:**
    * [x] Add GitHub Models (Llama 3, Phi-3, Claude) as a new AI backend in the bot.
    * [x] Implement auto-failover (if Gemini is down -> use GitHub Models).
    * [x] Добавить GitHub Models как новый бэкенд AI в боте.
    * [x] Реализовать авто-переключение (если Gemini лежит -> использовать GitHub Models).
3. **Automated Self-Healing / Автоматическое восстановление:**
    * [x] If a Pod fails in GKE, the bot reports the log to GitHub Issue automatically (`modules/self_healing.py`).
    * [x] The Agent (Me) analyzes the Issue using GitHub Models and prepares a fix.
    * [x] Если Под в GKE падает, бот сам создает Issue в GitHub с логами.
    * [x] Агент (Я) анализирует Issue через GitHub Models и готовит фикс.

---

## Execution Checklist / Чек-лист выполнения

* [x] Create Artifact Registry Repository (**Done**)
* [x] Create `.github/workflows/deploy.yaml` (**Done**)
* [x] Register GitHub Models API in the bot logic (**Done**)
* [x] Provision GCP Secret Manager secrets (**Done**)
* [x] Update GKE Deployment manifests to bind Secrets (**Done**)
* [x] Grant permissions to Kostik (sys-admin level) (**Done**)
* [x] Implement AI provider failover to GitHub Models (**Done**)
* [ ] Integrate GustavoASC.google-drive-vscode (manual reset needed).
* [x] Resolve Bot Instance Conflicts (Stopped rogue processes) (**Done**)
* [x] Repair Content Factory cloud deployment (Paths & Deps) (**Done**)

---

## Phase 3: Observability, SLOs & Cost Guardrails / Фаза 3: Наблюдаемость, SLO

## и контроль затрат

1. **Unified Logging & Metrics / Единые логи и метрики:**
    * [x] Wire Cloud Logging + Cloud Monitoring dashboards per service; ship
        structured logs (JSON) with trace ids.
    * [x] Настроить Cloud Logging и Cloud Monitoring с дашбордами по сервисам;
        логировать JSON со trace id.
2. **SLOs & Alerts / SLO и алерты:**
    * [x] Define availability/latency SLOs; create alerting policies to
        Telegram/Slack via webhooks.
    * [x] Определить SLO по доступности/задержке; завести алерты в Telegram/Slack
        через вебхуки.
3. **Tracing & Profiling / Трейсинг и профилирование:**
    * [x] Enable OpenTelemetry exporters (HTTP + background workers) into Cloud
        Trace/Profiler.
    * [x] Включить OpenTelemetry экспорт (HTTP + фоновые воркеры) в Cloud
        Trace/Profiler.
4. **FinOps Guardrails / Финансовые ограничения:**
    * [x] Budgets with 50/75/90% alerts; per-namespace quotas; scheduled
        scale-to-zero for non-prod.
    * [x] Бюджеты с алертами на 50/75/90%; квоты на namespace; автоскейл до нуля
        для non-prod по расписанию.

## Phase 4: Security Hardening & Supply Chain / Фаза 4: Усиление безопасности

## и цепочки поставок

1. **IAM & Network Policy / IAM и сетевые политики:**
    * [x] Enforce least-privilege roles; Namespace RBAC + NetworkPolicy to isolate
        services.
    * [x] Минимизировать роли; включить Namespace RBAC и NetworkPolicy для изоляции
        сервисов.
2. **Image & SBOM Hygiene / Гигиена образов и SBOM:**
    * [x] Automate SBOM (Syft) + vulnerability scan (Grype) in GitHub Actions.
    * [x] Enable Container Analysis API for Artifact Registry.
    * Автоматизировать SBOM (Syft) и скан уязвимостей (Grype/Artifact Analysis)
        в CI.
3. **Binary Authorization / Бинарная авторизация:**
    * [x] Enable Binary Authorization on GKE Autopilot (PROJECT_SINGLETON_POLICY).
    * [x] Configure Attestors and Policy (`policy.yaml` enforced).
    * [x] Требовать подписанные аттестации образов из CI; блокировать неподписанные деплои в GKE.
4. **Secrets Hygiene / Гигиена секретов:**
    * 90-day rotation policy; automated drift detection between Secret Manager
        and manifests.
    * Политика ротации каждые 90 дней; авто-детект дрейфа между Secret Manager
        и манифестами.

## Phase 5: Developer Experience & Runbooks / Фаза 5: Опыт разработчиков и инструкции

1. **Golden Paths / Золотые пути:**
   * [ ] Coordinate with Igor about secondary port allocations for new services
     and extensions.
   * [x] Repo templates for new services (`templates/python-microservice`).
   * [x] Шаблоны репозитория для новых сервисов (`templates/python-microservice`).
2. **Preview Environments / Превью окружения:**
   * [x] Ephemeral namespaces per PR (`templates/.../workflows/preview.yaml`).
   * [x] Эфемерные namespace на PR (`templates/.../workflows/preview.yaml`).
3. **Incident Runbooks / Ранбуки инцидентов:**
   * [x] Created `docs/runbooks/INCIDENT_RESPONSE.md`.
   * [x] Created `.github/ISSUE_TEMPLATE/incident_report.md`.

## Phase 6: Advanced Integrations & Security (H1 2026) / Фаза 6: Интеграции и Безопасность

**Goal:** Leverage AI agents (Antigravity), Firebase MCP, and external security auditing.
**Цель:** Использование AI агентов, Firebase MCP и внешнего аудита безопасности.

1. **Firebase MCP Server / Сервер Firebase MCP:**
    * [x] Implement `mcp_config.json` for seamless integration with AI agents.
    * [x] Enable Firebase MCP features for project management.
2. **Gemini Code Assist / Ассистент Gemini:**
    * [x] Enable `cloudaicompanion.googleapis.com` API.
    * [ ] Verify IDE integration (manual user step).
3. **VirusTotal Security Pipeline / Пайплайн безопасности VirusTotal:**
    * [x] Implement `scripts/security/scan_release.py` (Zip + Hash + VT Check).
    * [x] Integrate into "Release" workflow (GitHub Actions).
4. **Notion & Copilot / Notion и Copilot:**
    * [x] Verify Notion integration status (Key Present).
    * [x] Create `COPILOT_INSTRUCTIONS.md` for team-wide context.

---

## Rolling 3-Week Plan (starting 2026-02-11) / План на 3 недели (с 2026-02-11)

* **Week 1 (Feb 11–14, 2026):** Dashboards + alerting to Telegram/Slack; enable
    OTel exporters; set GCP budgets.
* **Неделя 1 (11–14 фев 2026):** Дашборды и алерты в Telegram/Slack; включить
    OTel; задать бюджеты GCP.
* **Week 2 (Feb 17–21, 2026):** NetworkPolicy + RBAC tightening; CI SBOM + vuln
    scans; Binary Authorization pilot.
* **Неделя 2 (17–21 фев 2026):** NetworkPolicy/RBAC; SBOM и сканы в CI; пилот
    Binary Authorization.
* **Week 3 (Feb 24–28, 2026):** Preview envs per PR; drift detection for
    secrets; publish incident runbooks & templates.
* **Неделя 3 (24–28 фев 2026):** Превью окружения; детект дрейфа секретов;
    публикация ранбуков и шаблонов.

---

## Risks & Mitigations / Риски и меры

* **Budget overruns / Перерасход бюджета:** hard budgets + weekly cost report;
    autoscale-to-zero non-prod nights/weekends.
* **Security drift / Утечка безопасности:** CIS Benchmarks in CI + weekly
    `gcloud` policy scan; alert on new public endpoints.
* **Vendor lock / Зависимость от провайдера:** maintain GitHub Models + Gemini
    dual-path; keep k8s manifests cloud-agnostic.
* **Alert fatigue / Шум алертов:** start with SLO-based alerts only; monthly
    tuning based on burn-rate reports.
