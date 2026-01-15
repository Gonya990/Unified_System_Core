# Задача: Реализация RBAC в AI Core и Сетевая Оркестрация

> **ID Сессии:** df92b102-rbac-412c-af77-ai_core_secure
> **Дата:** 2026-01-15
> **Статус:** 🔄 В Работе

## 🎯 Основная цель

Валидация и завершение реализации системы контроля доступа (RBAC) для AI Core,
проверка сетевой оркестрации и регистрация устройств.

## 📋 План действий <!-- id: 100 -->

### Фаза 1: Анализ и Аудит <!-- id: 101 -->

- [x] Проанализировать структуру `Projects/AI_Core` на наличие <!-- id: 101a -->
      RBAC кода
- [x] Проверить последние изменения (commit `976daef`) <!-- id: 101b -->
- [x] Определить текущий статус сборки Docker образа <!-- id: 101c -->

### Фаза 2: Реализация и Валидация <!-- id: 102 -->

- [x] Проверить скрипты регистрации сетевых устройств <!-- id: 102a -->
- [x] Валидация RBAC для Vertex AI Discovery Engine <!-- id: 102b -->
- [x] Тестирование системы разрешений (`init_rbac.py` passed) <!-- id: 102c -->

### Фаза 3: Оркестрация <!-- id: 103 -->

- [x] Обновить документацию по безопасности (`AGENTS_LEARNING_SCHEME.md` created) <!-- id: 103a -->
- [x] Синхронизация изменений (Fixed `InvalidToken` bug, Service Active) <!-- id: 103b -->
      > **Note**: `telegram.error.Conflict` detected. Rogue instance on `unified-home-core` (100.110.209.49) is fighting for the token.
      > **Action**: Reboot `unified-home-core` or fix Tailscale ACLs to allow SSH.
