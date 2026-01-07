# 🔥 Критические Проблемы - Варианты Лечения

> Дата: 2026-01-07 18:01 EET  
> Генератор: Antigravity Agent

---

## 📊 Диагностика Завершена

### Проблема 1: Git Repository Corruption ⚠️

**Статус**: Ложная тревога! Git работает корректно.

- Remote: ✅ Настроен правильно (`git@github.com:Gonya990/Unified_System_Core.git`)
- Branch: ✅ `main` существует
- **Корневая причина**: Подмодуль `External_Tools/Stack/mcp_agent_mail` имеет локальные изменения

### Проблема 2: Disk Space 84% 🔴

**Статус**: Критично! Основная проблема найдена.

#### 🎯 Главные потребители места

```
28 GB  - /home/gonya/ContentFarm ⚠️ САМЫЙ БОЛЬШОЙ
8.1 GB - /home/gonya/projects
1.3 GB - /home/gonya/Unified_System (текущая папка)
529 MB - /home/gonya/Unified_System_Core (дубликат?)
201 MB - /var/log/journal
113 MB - google-chrome-stable_current_amd64.deb (установщик)
```

**Итого потенциально освобождается**: ~35-40 GB

---

## 🛠️ Варианты Лечения

### 🎯 Проблема 1: Git Repository (Подмодуль)

#### Вариант A: Быстрый Reset (Рекомендуется)

**Действие**: Сбросить изменения в подмодуле  
**Риск**: Низкий (потеряются uncommitted изменения в подмодуле)  
**Время**: 30 секунд

```bash
cd /home/gonya/Unified_System/External_Tools/Stack/mcp_agent_mail
git reset --hard HEAD
git clean -fd
```

#### Вариант B: Сохранить изменения

**Действие**: Закоммитить изменения в подмодуле  
**Риск**: Нет  
**Время**: 2 минуты

```bash
cd /home/gonya/Unified_System/External_Tools/Stack/mcp_agent_mail
git status
git add -A
git commit -m "Save local changes"
```

#### Вариант C: Обновить подмодуль

**Действие**: Синхронизировать с upstream  
**Риск**: Средний (могут появиться конфликты)  
**Время**: 1 минута

```bash
cd /home/gonya/Unified_System
git submodule update --remote --merge External_Tools/Stack/mcp_agent_mail
```

---

### 🎯 Проблема 2: Disk Space

#### 🥇 Вариант 1: ContentFarm Cleanup (Освобождает ~28 GB)

##### План A: Полное удаление

**Риск**: 🔴 Высокий - потеря всех данных  
**Освобождается**: ~28 GB

```bash
# ОПАСНО! Сначала проверить содержимое
du -sh /home/gonya/ContentFarm/*
ls -lah /home/gonya/ContentFarm/

# Если не нужно - удалить
rm -rf /home/gonya/ContentFarm
```

##### План B: Архивирование важных данных

**Риск**: 🟡 Средний  
**Освобождается**: ~25 GB (после архивации)

```bash
# Создать архив
cd /home/gonya
tar -czf ContentFarm_backup_$(date +%Y%m%d).tar.gz ContentFarm/

# Переместить в безопасное место
# Затем удалить оригинал
rm -rf ContentFarm/
```

##### План C: Выборочная очистка

**Риск**: 🟢 Низкий  
**Освобождается**: ~15-20 GB

```bash
# Найти большие файлы в ContentFarm
find /home/gonya/ContentFarm -type f -size +100M -exec ls -lh {} \;

# Удалить старые логи
find /home/gonya/ContentFarm -name "*.log" -mtime +7 -delete

# Удалить кэш и временные файлы
find /home/gonya/ContentFarm -name "__pycache__" -o -name "*.pyc" -exec rm -rf {} +
find /home/gonya/ContentFarm -name ".cache" -type d -exec rm -rf {} +
```

---

#### 🥈 Вариант 2: Projects Cleanup (Освобождает ~5-8 GB)

```bash
# Анализ содержимого
du -sh /home/gonya/projects/*

# Удаление неиспользуемых venv
find /home/gonya/projects -name "venv" -o -name ".venv" -type d

# Удаление node_modules (если есть)
find /home/gonya/projects -name "node_modules" -type d

# Очистка кэша
find /home/gonya/projects -name "__pycache__" -type d -exec rm -rf {} +
```

---

#### 🥉 Вариант 3: Системная Очистка (Освобождает ~1-2 GB)

```bash
# Очистка APT кэша
sudo apt clean
sudo apt autoclean
sudo apt autoremove -y

# Удаление старых логов
sudo journalctl --vacuum-time=7d
sudo find /var/log -name "*.log.*" -delete
sudo find /var/log -name "*.gz" -delete

# Удаление установщиков
rm -f /home/gonya/*.deb

# Очистка tmp
sudo rm -rf /tmp/*
```

---

#### 🎁 Вариант 4: Дубликаты (Освобождает ~529 MB)

```bash
# Проверить, является ли Unified_System_Core дубликатом
diff -r /home/gonya/Unified_System /home/gonya/Unified_System_Core

# Если это старая копия - удалить
rm -rf /home/gonya/Unified_System_Core
```

---

## 🎯 Рекомендуемый План Действий

### 🚀 Быстрое Решение (5 минут, освобождает ~30+ GB)

1. **Проверить ContentFarm** (что это)
2. **Удалить установщики** (113 MB)
3. **Очистить системные логи** (~1 GB)
4. **Удалить дубликат Unified_System_Core** (529 MB)
5. **Сбросить подмодуль git** (исправить git статус)

```bash
# Шаг 1: Проверка ContentFarm
ls -lah /home/gonya/ContentFarm/

# Шаг 2: Удаление установщиков
rm -f /home/gonya/*.deb

# Шаг 3: Системная очистка
sudo apt clean && sudo apt autoremove -y
sudo journalctl --vacuum-time=7d

# Шаг 4: Дубликат (если подтвердится)
# rm -rf /home/gonya/Unified_System_Core

# Шаг 5: Git fix
cd /home/gonya/Unified_System/External_Tools/Stack/mcp_agent_mail
git reset --hard HEAD
```

---

### 🏆 Агрессивное Решение (10 минут, освобождает ~35-40 GB)

```bash
# Все из быстрого решения +
# Удаление ContentFarm (если не критично)
tar -czf /tmp/ContentFarm_backup.tar.gz /home/gonya/ContentFarm
rm -rf /home/gonya/ContentFarm

# Очистка projects
find /home/gonya/projects -name "venv" -o -name ".venv" | xargs rm -rf
find /home/gonya/projects -name "node_modules" | xargs rm -rf
```

---

## ⚠️ Важные Предупреждения

1. **ContentFarm (28 GB)**:
   - ⚠️ Проверить, есть ли там ценные данные!
   - Возможно, это старая версия Video Factory?
   - **Действие**: Сначала просмотреть содержимое

2. **Unified_System_Core (529 MB)**:
   - Похоже на дубликат текущей папки
   - **Действие**: Проверить с помощью `diff`

3. **Подмодуль git**:
   - Сейчас работает (mcp_agent_mail запущен)
   - **Действие**: Сбросить безопасно

---

## 🎬 Следующие Шаги

Выберите один из планов:

- **A) Консервативный** (освобождает ~3-5 GB, безопасно)
- **B) Умеренный** (освобождает ~15-20 GB, проверка ContentFarm)
- **C) Агрессивный** (освобождает ~35+ GB, удаление ContentFarm)

Я готов выполнить любой план по вашей команде! 🚀

---

*Antigravity Agent готов к действию*
