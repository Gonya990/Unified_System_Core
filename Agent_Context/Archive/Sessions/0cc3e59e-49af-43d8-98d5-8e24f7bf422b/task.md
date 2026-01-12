# ИНИЦИАЛИЗАЦИЯ NODE-01 (ANTIGRAVITY HUB)

## Фаза 1: Физическая сборка (Hardware) <!-- id: 100 -->

- [x] RAM: Проверка установки Corsair Vengeance в слоты A2/B2 <!-- id: 101 -->
- [x] GPU: Подключение Titan RTX (2x8 pin PCI-E) <!-- id: 102 -->
- [x] PiKVM: Коммутация с Front Panel (PW_SW) и HDMI-OUT <!-- id: 103 -->
- [x] Охлаждение: Проверка направления потоков в 4U корпусе <!-- id: 104 -->

## Фаза 2: Настройка BIOS/Firmware (ACTIVE) <!-- id: 200 -->

- [x] Исследование: Web research для SVM, Above 4G, Re-size BAR <!-- id: 205 -->
- [x] Документация: Создан BIOS_CONFIGURATION_GUIDE.md <!-- id: 206 -->
- [x] Аудит оборудования: ASUS ROG STRIX X370-F GAMING, BIOS 5220, CPU Ryzen 5 3600X <!-- id: 207 -->
- [/] Выполнение: Настройка через PiKVM <!-- id: 201 --> <!-- CURRENT FOCUS -->
  - [ ] **BIOS Update:** Flash version 6203 (Stable) <!-- id: 201a -->
  - [ ] **SVM Mode (CPU Features):** Enable (Advanced -> CPU -> SVM/AMD-V) <!-- id: 202 -->
  - [ ] **Above 4G Decoding:** Enable (Advanced -> PCI/Chipset) <!-- id: 203 -->
  - [ ] **Re-size BAR:** Auto/Enabled (REQUIRES CSM DISABLED) <!-- id: 203a -->
  - [ ] **Power Policy:** Power On (AC Back/Restore on AC Power Loss) <!-- id: 204 -->
  - [ ] **IOMMU:** Enable (for Proxmox Passthrough) <!-- id: 204a -->

## Фаза 3: Развертывание ОС и Сети (DONE) <!-- id: 300 -->

- [x] Установка Windows 11 Pro / Ubuntu Server <!-- id: 301 -->
- [x] Инсталляция NVIDIA Studio Drivers & CUDA toolkit <!-- id: 401 -->
- [x] Настройка Tailscale Mesh VPN <!-- id: 302 -->
- [x] Конфигурация OpenSSH Server <!-- id: 303 -->

## Фаза 4: AI Стек (DONE) <!-- id: 400 -->

- [x] WSL 2 + Docker Engine Setup <!-- id: 401 -->
- [x] Deployment: Ollama (LLM API) <!-- id: 402 -->
- [x] Visual Verification: n8n Dashboard captured & Account Verified (Welcome Screen) <!-- id: 524 -->
- [x] DRY RUN (NODE-01): n8n ✅, Ollama ✅, Chrome ✅, Ports ⚠️ (Firewall check needed) <!-- id: 507 -->

## ПРИОРИТЕТНАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ (ACTIVE) <!-- id: 600 -->

- [x] PHASE 1: BROWSER AGENT ACTIVATION (Scripts/browser_agent.py -> Windows) <!-- id: 601 -->
- [x] PHASE 2: PROXMOX RECONNAISSANCE (Connectivity Check - Node Offline) <!-- id: 602 -->
- [/] PHASE 3: STRATEGIC CREDENTIAL EXTRACTION (Quick Path ✅ / Full Path ⚠️ Chrome Crash) <!-- id: 603 -->
  - [x] Path A: Gemini API Key activation (OPERATIONAL) <!-- id: 603a -->
  - [ ] Path B: Service Account JSON extraction (BLOCKED - Chrome crash) <!-- id: 603b -->

## ФАЗА 5: OMNISCIENCE & HIVE-MIND (IN PROGRESS) <!-- id: 500 -->

- [x] Принятие протокола "GRAND UNIFICATION" (RC) <!-- id: 511 -->
- [x] Infrastructure: Windows Firewall & Chrome Debugging (0.0.0.0) <!-- id: 512 -->
- [x] Верификация: curl 100.127.194.111:9222/json/version (Verified) <!-- id: 513 -->
- [x] Fix n8n Cloud: "MCP Windows (Tailscale)" JS-RPC 2.0 <!-- id: 505 -->
- [x] Роутинг: Fractal Agent Deployment (Deployment of Sub-Agents) <!-- id: 509 -->
- [x] Gemini Cloud Brain: API активирован (26 models available) <!-- id: 515 -->
- [x] Исследование: Chrome crash solutions (web research complete) <!-- id: 516 -->
- [x] Chrome Restart: Выполнен с флагами стабильности (HeadlessChrome/124.0.6367.78) <!-- id: 518 -->
- [ ] **NEW BLOCKER:** Credential extraction timeout (180s WebSocket, not crash) <!-- id: 519 -->
  - Альтернативы: Manual download, gcloud CLI, increased timeout
  - Документация: CHROME_RESTART_POSTMORTEM.md
- [/] Подключение Google Workspace & GitHub (BLOCKED - timeout issue) <!-- id: 501 -->
- [ ] Интеграция Apple API (Keys extraction via Windows) <!-- id: 502 -->
- [x] Аудит оборудования NODE-01: RTX 3080 10GB (Driver 581.57) <!-- id: 506 -->
- [x] System Readiness Check: GPU/VRAM/RAM/Services verified for 24/7 operation <!-- id: 517 -->
- [x] **ФИЗИЧЕСКИЙ ДОСТУП (Serial):** Restore SSH Access (Firewall) <!-- id: 526 -->
- [x] Proxmox Audit: ONLINE, Web UI accessible, требуются credentials для hardware specs <!-- id: 602 -->
  - Документация: PROXMOX_AUDIT_REPORT.md
  - Screenshot: proxmox_login_page_1766131961216.png
- [x] Native SSH Verification: `ssh igor-gaming-1` (OK), `ssh igor-windows` (Password OK) <!-- id: 522 -->
- [x] System Wide Audit: GPU/CPU/RAM verified (See SYSTEM_FULL_AUDIT.md) <!-- id: 523 -->
- [x] Запуск "Сухой прогонки" (Анализ) и финальный подъем <!-- id: 507 -->
- [x] Telegram Bot: Credentials configured (Token + ChatID 708531393) <!-- id: 520 -->
- [x] Google/Apple Integration: Docker Auth SUCCESS (User: <gonya90.gg@gmail.com>) <!-- id: 521 -->
  - [x] SSH Connection Restored
  - [x] Generate Auth Link
  - [x] Submit Code
- [x] Find Patch/Tool: Used "Docker on NODE-01" to bypass missing SDK <!-- id: 525 -->
