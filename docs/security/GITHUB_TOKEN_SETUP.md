# 🔐 GitHub Token Security - Пошаговая Инструкция

## ⚠️ КРИТИЧЕСКИ ВАЖНО - ВЫПОЛНИТЬ НЕМЕДЛЕННО!

Ваш GitHub Personal Access Token был скомпрометирован. Следуйте этим шагам:

---

## 📋 ШАГ 1: ОТЗЫВ СТАРОГО ТОКЕНА

### Откройте браузер и перейдите:
```
https://github.com/settings/tokens
```

### Действия:
1. Найдите токен, который начинается с `ghp_uMomvhW0Hi6Y4i9rf4yABkJbKK79jS...`
2. Нажмите **"Delete"** или **"Revoke"** рядом с этим токеном
3. Подтвердите удаление

---

## 📋 ШАГ 2: СОЗДАНИЕ НОВОГО ТОКЕНА

### Откройте:
```
https://github.com/settings/tokens/new
```

### Настройки нового токена:

**Note (название токена):**
```
Antigravity IDE - MacBook Air - 2026
```

**Expiration (срок действия):**
- Выберите: `90 days` (рекомендуется) или `No expiration` (если нужен永久)

**Scopes (права доступа):**

✅ **Обязательные права для IDE:**
- [x] `repo` - Полный доступ к репозиториям
  - [x] `repo:status` - Статус коммитов
  - [x] `repo_deployment` - Деплойменты
  - [x] `public_repo` - Публичные репозитории
  - [x] `repo:invite` - Приглашения
  - [x] `security_events` - События безопасности

- [x] `workflow` - Управление GitHub Actions

- [x] `read:org` - Чтение организаций
  - [x] `read:project` - Чтение проектов

- [x] `user` - Доступ к профилю
  - [x] `read:user` - Чтение профиля
  - [x] `user:email` - Email адреса
  - [x] `user:follow` - Подписки

✅ **Опционально (рекомендуется):**
- [x] `gist` - Создание gists
- [x] `notifications` - Уведомления
- [x] `read:discussion` - Обсуждения

❌ **НЕ ВКЛЮЧАЙТЕ (опасно):**
- [ ] `delete_repo` - Удаление репозиториев
- [ ] `admin:public_key` - Управление SSH ключами

### Создайте токен:
1. Прокрутите вниз
2. Нажмите **"Generate token"**
3. **СКОПИРУЙТЕ ТОКЕН СРАЗУ!** (он больше не покажется)

---

## 📋 ШАГ 3: СОХРАНЕНИЕ НОВОГО ТОКЕНА

### Используйте автоматический скрипт:

```bash
/Users/igorgoncharenko/Documents/Unified_System_Core/Scripts/Tools/github-token-setup.sh
```

Или добавьте alias:
```bash
alias gh-token="/Users/igorgoncharenko/Documents/Unified_System_Core/Scripts/Tools/github-token-setup.sh"
```

### В скрипте выберите:
- **Опция 2**: Проверить новый токен (сначала проверка)
- **Опция 3**: Сохранить новый токен в ~/.zshrc (после проверки)

### Или вручную:

1. Откройте терминал
2. Выполните:
   ```bash
   nano ~/.zshrc
   ```
3. Найдите строку:
   ```bash
   export GITHUB_TOKEN="ЗАМЕНИТЕ_НА_НОВЫЙ_ТОКЕН_ПОСЛЕ_ОТЗЫВА"
   ```
4. Замените на:
   ```bash
   export GITHUB_TOKEN="ваш_новый_токен_сюда"
   ```
5. Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`
6. Примените:
   ```bash
   source ~/.zshrc
   ```

---

## 📋 ШАГ 4: ПРОВЕРКА НАСТРОЙКИ

### Проверьте переменную:
```bash
echo $GITHUB_TOKEN
```

### Проверьте доступ к GitHub:
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

Должны увидеть ваш логин и информацию о пользователе.

### Или используйте скрипт:
```bash
/Users/igorgoncharenko/Documents/Unified_System_Core/Scripts/Tools/github-token-setup.sh
```
Выберите **опцию 1** для проверки.

---

## 📋 ШАГ 5: НАСТРОЙКА GIT CREDENTIAL HELPER

Уже настроено! ✅
```bash
git config --global credential.helper osxkeychain
```

При следующем `git push` или `git pull`:
- **Username**: `Gonya990` (или ваш GitHub username)
- **Password**: вставьте новый токен (не пароль!)

---

## 🔗 БЫСТРЫЕ ССЫЛКИ

| Действие | Ссылка |
|----------|--------|
| 🗑️ Отозвать токены | https://github.com/settings/tokens |
| ➕ Создать новый токен | https://github.com/settings/tokens/new |
| 👤 Профиль GitHub | https://github.com/settings/profile |
| 📧 Email настройки | https://github.com/settings/emails |
| 🔐 Двухфакторная аутентификация | https://github.com/settings/security |

---

## ✅ CHECKLIST

- [ ] Старый токен отозван
- [ ] Новый токен создан с правильными правами
- [ ] Новый токен скопирован
- [ ] Токен проверен через скрипт (опция 2)
- [ ] Токен сохранен в ~/.zshrc (опция 3)
- [ ] Выполнен `source ~/.zshrc`
- [ ] Проверен доступ к GitHub API
- [ ] Первый git push выполнен успешно

---

## 💡 ВАЖНЫЕ СОВЕТЫ

1. **Никогда не публикуйте токены** в коде, чатах, или документации
2. **Используйте переменные окружения** для хранения секретов
3. **Регулярно обновляйте токены** (каждые 90 дней)
4. **Используйте минимальные необходимые права**
5. **Включите 2FA** на GitHub для дополнительной безопасности

---

## 🆘 ПОМОЩЬ

Если что-то не работает, запустите:
```bash
/Users/igorgoncharenko/Documents/Unified_System_Core/Scripts/Tools/github-token-setup.sh
```

Опция 5 покажет все рекомендуемые права.

---

**Создано:** 2026-01-29  
**Для:** Igor Goncharenko (@Gonya990)  
**Система:** Unified System Core - Antigravity IDE
