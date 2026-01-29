# Chrome DevTools MCP - Руководство пользователя

## 🎯 Что такое Chrome DevTools MCP?

**Chrome DevTools MCP (Model Context Protocol)** — это специальный сервер, который позволяет AI-ассистентам (например, Antigravity IDE) взаимодействовать с Chrome DevTools программно. Это открывает возможности для:

- 🔍 **Автоматической отладки** веб-приложений через AI
- 📊 **Анализа производительности** с помощью AI
- 🐛 **Поиска и исправления ошибок** в консоли
- 🌐 **Инспектирования сетевых запросов**
- 💾 **Управления cookies, storage, cache**
- 🎨 **Анализа и модификации CSS/DOM**

---

## 📦 Установка

### Автоматическая установка (✅ Уже выполнено!)

```bash
cd ~/Documents/Unified_System_Core/Tools
git clone https://github.com/ChromeDevTools/chrome-devtools-mcp.git
cd chrome-devtools-mcp
npm install
npm run build
```

### Быстрый доступ через alias

Добавьте в `~/.zshrc`:

```bash
alias devtools-mcp="~/Documents/Unified_System_Core/Tools/chrome-devtools-mcp/devtools-mcp.sh"
```

Затем:

```bash
source ~/.zshrc
```

---

## 🚀 Быстрый старт

### Способ 1: Автоматический режим (рекомендуется)

**Новая функция в v0.12.1!** Auto-attach позволяет подключиться к уже работающему Chrome:

```bash
# Шаг 1: Запустите Chrome обычным способом
open -a "Google Chrome" --args --remote-debugging-port=9222

# Шаг 2: Запустите MCP Server
devtools-mcp server
```

MCP Server автоматически подключится к существующей сессии браузера!

### Способ 2: Полный контроль

```bash
# Запустить Chrome в режиме отладки
devtools-mcp chrome

# В другом терминале запустить MCP Server
devtools-mcp server
```

### Способ 3: Всё сразу

```bash
devtools-mcp all
```

---

## 📋 Команды управления

| Команда | Короткая | Описание |
|---------|----------|----------|
| `devtools-mcp chrome` | `c` | Запустить Chrome с remote debugging |
| `devtools-mcp server` | `s` | Запустить MCP Server |
| `devtools-mcp build` | `b` | Собрать проект |
| `devtools-mcp status` | `st` | Проверить состояние |
| `devtools-mcp stop` | - | Остановить Chrome |
| `devtools-mcp restart` | `r` | Перезапустить Chrome |
| `devtools-mcp examples` | `e` | Показать примеры |
| `devtools-mcp all` | `a` | Собрать и запустить всё |

---

## ⚙️ Интеграция с Antigravity IDE

### MCP Server Configuration

Добавьте в настройки Antigravity IDE:

**Путь:** `Настройки > MCP Servers` или в файл конфигурации IDE

```json
{
  "mcp.servers": {
    "chrome-devtools": {
      "command": "node",
      "args": [
        "/Users/igorgoncharenko/Documents/Unified_System_Core/Tools/chrome-devtools-mcp/build/index.js"
      ],
      "env": {
        "CHROME_PATH": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
      }
    }
  }
}
```

### Использование в IDE

После настройки вы сможете:

1. **Попросить AI отладить сайт:**

   ```
   "Проанализируй производительность https://example.com"
   "Найди ошибки в консоли на текущей странице"
   "Покажи все сетевые запросы к API"
   ```

2. **Анализировать trace файлы:**

   ```
   "Проанализируй trace и найди узкие места"
   "Почему страница тормозит при скролле?"
   ```

3. **Модифицировать страницу:**

   ```
   "Измени цвет кнопки на синий"
   "Добавь border к элементу .header"
   ```

---

## 🔧 Продвинутое использование

### 1. Auto-Attach к существующей сессии

```bash
# Откройте Chrome как обычно, но с флагом отладки
open -a "Google Chrome" --args --remote-debugging-port=9222

# MCP подключится к этой сессии автоматически
devtools-mcp server
```

**Преимущества:**

- ✅ Сохраняются все ваши расширения
- ✅ Работает с вашим профилем
- ✅ Можете продолжить работу с того места, где остановились

### 2. Тестирование подключения

```bash
# Проверьте, что Chrome принимает подключения
curl http://localhost:9222/json

# Вы должны увидеть JSON с информацией о вкладках
```

### 3. Отладка конкретной вкладки

```bash
# Получите список вкладок
curl http://localhost:9222/json | jq '.[].title'

# Подключитесь через WebSocket URL
# (MCP Server делает это автоматически)
```

### 4. Использование с Docker/Remote Chrome

```bash
# Запустите Chrome в Docker
docker run -d -p 9222:9222 \
  --name chrome-debug \
  zenika/alpine-chrome \
  --remote-debugging-address=0.0.0.0 \
  --remote-debugging-port=9222

# Подключите MCP Server
devtools-mcp server
```

---

## 🎨 Примеры использования с AI

### Анализ производительности

**Вопрос к AI:**

```
Открой https://myapp.com и проанализируй:
1. Время загрузки страницы
2. Размер всех ресурсов
3. Узкие места в производительности
```

**AI может:**

- Запустить Performance trace
- Проанализировать LCP, CLS, FID
- Найти медленные запросы
- Предложить оптимизации

### Отладка ошибок

**Вопрос к AI:**

```
Проверь консоль на ошибки и исправь их
```

**AI может:**

- Читать console.error
- Анализировать stack traces
- Предлагать исправления
- Применять фиксы через Workspaces

### Тестирование API

**Вопрос к AI:**

```
Покажи все запросы к /api/users и их response time
```

**AI может:**

- Фильтровать Network requests
- Анализировать headers
- Проверять payload
- Измерять timing

---

## 🔒 Безопасность

### Важные заметки

⚠️ **Remote debugging mode открывает порт 9222**

- Используйте только в локальной разработке
- Не открывайте порт в интернет
- Закрывайте Chrome после отладки

### Рекомендации

1. **Используйте firewall:**

   ```bash
   # Блокируйте внешние подключения к 9222
   sudo pfctl -e
   ```

2. **Работайте с staging/dev окружениями**
   - Не используйте production credentials
   - Используйте test accounts

3. **Очищайте данные после отладки:**

   ```bash
   # User data хранится в ~/.chrome-devtools-mcp
   rm -rf ~/.chrome-devtools-mcp
   ```

---

## 📊 Мониторинг и логи

### Проверка состояния

```bash
devtools-mcp status
```

Выведет:

- ✅ Статус Chrome (работает/не работает)
- 📄 Количество открытых вкладок
- 🔨 Статус MCP Server (собран/не собран)
- ⚙️ Найденные конфигурации

### Логи MCP Server

```bash
# Запустите server с выводом логов
node ~/Documents/Unified_System_Core/Tools/chrome-devtools-mcp/build/index.js
```

### Логи Chrome

```bash
# Chrome выводит логи в:
tail -f /Users/igorgoncharenko/Library/Application\ Support/Google/Chrome/chrome_debug.log
```

---

## 🐛 Устранение неполадок

### Chrome не запускается

```bash
# Проверьте, не занят ли порт
lsof -ti:9222

# Убейте процесс если нужно
kill $(lsof -ti:9222)

# Попробуйте заново
devtools-mcp chrome
```

### MCP Server не подключается

```bash
# Убедитесь, что Chrome запущен с правильными флагами
ps aux | grep chrome | grep remote-debugging-port

# Проверьте доступность порта
curl http://localhost:9222/json
```

### Ошибки при сборке

```bash
# Переустановите зависимости
cd ~/Documents/Unified_System_Core/Tools/chrome-devtools-mcp
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📚 Полезные ссылки

- 📖 [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- 🔧 [MCP GitHub Repository](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- 📝 [Changelog](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/CHANGELOG.md)
- 🌐 [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- 🎓 [DevTools 144 Release Notes](https://developer.chrome.com/blog/new-in-devtools-144)

---

## 🆘 Получить помощь

### Через AI в IDE

```
Помоги мне настроить Chrome DevTools MCP
Как использовать auto-attach?
Покажи примеры отладки с MCP
```

### Скрипт помощи

```bash
devtools-mcp examples
```

### Логи для диагностики

```bash
# Полная диагностика
devtools-mcp status
lsof -ti:9222
curl http://localhost:9222/json
```

---

## ✅ Чек-лист настройки

- [x] Chrome DevTools MCP установлен
- [x] npm зависимости установлены
- [ ] Проект собран (`npm run build`)
- [ ] Alias добавлен в `~/.zshrc`
- [ ] MCP Server настроен в IDE
- [ ] Тестовое подключение выполнено
- [ ] Chrome запускается с remote debugging
- [ ] AI может взаимодействовать с DevTools

---

**Создано:** 2026-01-29  
**Для:** Igor Goncharenko - Unified System Core  
**Версия MCP:** 0.12.1  
**Chrome:** 144+
