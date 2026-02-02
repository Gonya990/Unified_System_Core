# 🔄 Repository Sync Guide

Этот документ описывает, как правильно работать с синхронизацией между репозиториями.

## 📍 Структура Remotes

```bash
origin           → Unified-system-Core/Unified_System_Core (основной)
antibridge_fixed → Gonya990/antibridge_fixed (зеркало)
```

## 🚀 Быстрый старт

### Автоматическая синхронизация

Используйте встроенный алиас для синхронизации всех remote:

```bash
git sync
```

Этот команда:

1. ✅ Fetch от всех remotes
2. ✅ Pull с rebase от origin/main
3. ✅ Push в origin/main
4. ✅ Push в antibridge_fixed/main (опционально)

### Ручная синхронизация

Если нужен больший контроль:

```bash
# 1. Fetch от всех
git fetch --all

# 2. Обновить локальную main
git checkout main
git pull origin main --rebase

# 3. Push в основной remote
git push origin main

# 4. Опционально: push в зеркало
git push antibridge_fixed main
```

## 📋 Повседневные операции

### Начать новую фичу

```bash
git checkout main
git pull origin main
git checkout -b feature/my-feature
# ... делайте изменения ...
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature
```

### Обновить main

```bash
git checkout main
git sync  # или git pull origin main --rebase
```

### Решить конфликты

```bash
# Если возник конфликт при pull
git status  # посмотрите конфликтные файлы
# Отредактируйте файлы, удалив маркеры конфликта
git add .
git rebase --continue
```

## ⚠️ Важные правила

### ✅ DO (Делать)

- ✅ Всегда работайте в отдельных ветках для фич
- ✅ Используйте `git sync` для синхронизации
- ✅ Делайте `git pull --rebase` вместо обычного pull
- ✅ Коммитьте часто с понятными сообщениями
- ✅ Проверяйте `.gitignore` перед commit

### ❌ DON'T (Не делать)

- ❌ НЕ коммитьте `.env` файлы
- ❌ НЕ коммитьте `node_modules/`
- ❌ НЕ делайте `git push --force` без необходимости
- ❌ НЕ коммитьте большие медиа файлы (используйте Git LFS)
- ❌ НЕ редактируйте историю уже запушенных веток

## 🛠️ Troubleshooting

### "Your branch has diverged"

```bash
git checkout main
git fetch origin
git reset --hard origin/main
```

### "Cannot push because remote contains work"

```bash
git pull origin main --rebase
git push origin main
```

### Откатить последний commit (локально)

```bash
git reset --soft HEAD~1  # Сохраняет изменения
# или
git reset --hard HEAD~1  # Удаляет изменения
```

### Очистить неотслеживаемые файлы

```bash
git clean -fd  # Удалить файлы и директории
git clean -fdn # Посмотреть, что будет удалено (dry-run)
```

## 🔧 Advanced

### Работа с submodules

```bash
# Обновить все submodules
git submodule update --init --recursive

# Обновить submodules до последней версии
git submodule update --remote
```

### Squash коммитов перед merge

```bash
git checkout feature/my-feature
git rebase -i HEAD~3  # Squash последние 3 коммита
# В редакторе замените 'pick' на 'squash' для коммитов, которые хотите объединить
```

### Cherry-pick коммита

```bash
git cherry-pick <commit-hash>
```

## 📚 Полезные алиасы

Добавьте в `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    sync = !bash .git-sync.sh
    lg = log --graph --oneline --all --decorate
    undo = reset --soft HEAD~1
```

## 🆘 Помощь

Если что-то пошло не так:

1. **Не паникуйте!** Git почти всегда можно восстановить
2. Проверьте статус: `git status`
3. Посмотрите историю: `git log --oneline`
4. Используйте `git reflog` для восстановления
5. Обратитесь к команде или создайте issue

---

**Last Updated:** 2026-02-02  
**Maintainer:** Igor Goncharenko
