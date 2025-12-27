# Быстрая Настройка Яндекс Алисы

## Шаг 1: Запуск Cloudflare Tunnel (на сервере igor-gaming-1)

```bash
# Подключитесь к серверу
ssh igor-gaming-1

# Запустите скрипт
bash /home/gonya/Documents/Unified_System/Scripts/automation/start_alice_tunnel.sh
```

Скрипт автоматически:

- Установит cloudflared (если нужно)
- Запустит туннель
- Покажет URL для настройки Яндекса

## Шаг 2: Настройка Навыка в Яндексе

1. Откройте: <https://dialogs.yandex.ru/developer/skills/e6dacdd4-f553-407e-a847-8be932d0d696/draft/settings/main>

2. В поле **"Webhook URL"** вставьте:

   ```
   https://ваш-url.trycloudflare.com/alice
   ```

   (URL из вывода скрипта выше)

3. Нажмите **"Сохранить"**

4. Перейдите на вкладку **"Тестирование"**

5. Попробуйте команды:
   - "Попроси Гоню включить свет"
   - "Попроси Гоню найти информацию о погоде"
   - "Попроси Гоню создать задачу купить молоко"

## Шаг 3: Постоянный Туннель (опционально)

Для автоматического запуска при перезагрузке:

```bash
# На сервере
sudo cp /home/gonya/Documents/Unified_System/Scripts/automation/alice-tunnel.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alice-tunnel
sudo systemctl start alice-tunnel

# Проверка
sudo systemctl status alice-tunnel
```

⚠️ **Важно:** URL от Cloudflare меняется при каждом перезапуске туннеля (если не используете Named Tunnel).
Для постоянного URL настройте Cloudflare Zero Trust (см. основную документацию).

## Примеры Команд для Алисы

- 🏠 **Умный дом**: "Попроси Гоню включить свет в гостиной"
- 🔍 **Поиск**: "Попроси Гоню найти рецепт борща"
- 📝 **Задачи**: "Попроси Гоню добавить задачу позвонить маме"
- 📊 **Статистика**: "Попроси Гоню показать статистику"
- 🌤 **Погода**: "Попроси Гоню какая погода в Киеве"

## Troubleshooting

**Алиса не отвечает:**

1. Проверьте, что бот запущен: `sudo systemctl status ai-bot`
2. Проверьте Alice Skill: `curl http://localhost:8090/health`
3. Проверьте туннель: `ps aux | grep cloudflared`

**Ошибка "Навык недоступен":**

- Убедитесь, что Webhook URL правильный
- Проверьте логи бота: `sudo journalctl -u ai-bot -f`

**Туннель отключается:**

- Используйте systemd сервис (Шаг 3)
- Или настройте Named Tunnel в Cloudflare Zero Trust
