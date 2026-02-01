# 🔑 ПОЛУЧЕНИЕ BYBIT API КЛЮЧЕЙ - ПОШАГОВО

**Статус:** Крипто-бот ЗАПУЩЕН, но нужны API keys! ⏳

---

## ✅ **ТЕКУЩИЙ СТАТУС:**

```
🤖 ByBit Trading Bot
Status: ONLINE (10+ минут)
Mode: TESTNET (безопасно!)
Problem: ❌ API keys не настроены
```

**Что делает сейчас:**

- Бот пытается подключиться
- Получает ошибку 401 (нет доступа)
- Ждёт API ключи
- **Trading paused** (торговля на паузе)

---

## 🎯 **ЧТО ДЕЛАТЬ - 2 ВАРИАНТА:**

### **ВАРИАНТ 1: HUMMINGBOT (УЖЕ ЕСТЬ!)** ⭐ РЕКОМЕНДУЮ

У тебя УЖЕ ЗАПУЩЕН Hummingbot 4 часа!
Там МОГУТ БЫТЬ ключи сохранены!

**Проверь:**

```bash
ssh unified-home-core-cloud
cd /home/gonya/hummingbot
cat conf/conf_global.yml | grep -i bybit
```

Если найдёшь ключи там → скопируй сюда!

---

### **ВАРИАНТ 2: СОЗДАТЬ НОВЫЕ КЛЮЧИ**

#### **Шаг 1: Зайди на ByBit**
<https://www.bybit.com/app/user/api-management>

#### **Шаг 2: Create New Key**

- System-generated API Keys
- **API Transaction** (NOT Funding!)

#### **Шаг 3: Permissions (ВАЖНО!)**

✅ **Включи:**

- Contract - Read only
- Spot - Read only  
- Spot - Trade (чтобы торговать)

❌ **НЕ ВКЛЮЧАЙ:**

- Withdraw (опасно!)
- Transfer (не нужно)

#### **Шаг 4: IP Restrict (БЕЗОПАСНОСТЬ)**

**Вариант А:** No restriction (проще, но менее безопасно)
**Вариант Б:** Add IP: `192.168.190.101` (твой сервер)

Узнай IP сервера:

```bash
ssh unified-home-core-cloud "curl -s ifconfig.me"
```

#### **Шаг 5: 2FA Code**

Введи код из Google Authenticator

#### **Шаг 6: СКОПИРУЙ КЛЮЧИ**

⚠️ **ВАЖНО! Покажи их только ОДИН РАЗ!**

- API Key: `xxxxxxxxxxxxxxxxx`
- API Secret: `yyyyyyyyyyyyyyyyyyy`

**СОХРАНИ В БЕЗОПАСНОМ МЕСТЕ!**

---

## 🔐 **ДОБАВЬ КЛЮЧИ В БОТ:**

```bash
ssh unified-home-core-cloud
nano /home/gonya/Unified_System_Core/Projects/AI_Core/.env
```

**Добавь в конец файла:**

```bash
# ByBit Trading Keys
BYBIT_API_KEY=твой_api_key_сюда
BYBIT_API_SECRET=твой_api_secret_сюда
```

**Сохрани:** Ctrl+O, Enter, Ctrl+X

---

## 🔄 **ПЕРЕЗАПУСТИ БОТА:**

```bash
pm2 restart crypto-bot
pm2 logs crypto-bot
```

**Должен показать:**

```
✅ ByBit Bot WORKS!
Balance: $XXX.XX USDT
State: Analyzing market...
```

---

## 💰 **TELEGRAM WALLET (АЛЬТЕРНАТИВА):**

Если хочешь торговать TON через Telegram Wallet:

1. Открой @wallet
2. Проверь баланс
3. Получи адрес

**НО!** Telegram Wallet API сложнее интегрировать.
**ByBit проще + больше возможностей!**

---

## 📊 **ЧТО СЛУЧИТСЯ ПОСЛЕ ДОБАВЛЕНИЯ КЛЮЧЕЙ:**

### **TESTNET Mode (сейчас):**

```
1. Бот подключится к ByBit Testnet
2. Получит виртуальный баланс ($100K USDT)
3. Начнёт виртуально торговать
4. Ты увидишь как работает
5. БЕЗ РИСКА!
```

**Рекомендую:** Протестируй 2-3 дня!

### **LIVE Mode (потом):**

```
1. Измени в коде: testnet=False
2. Перезапусти бота
3. Начнёт РЕАЛЬНУЮ торговлю
4. С НАСТОЯЩИМИ деньгами!
```

**Начинай с $20-30 MAX!**

---

## ⚠️ **БЕЗОПАСНОСТЬ:**

### **ОБЯЗАТЕЛЬНО:**

- ✅ 2FA на аккаунте ByBit
- ✅ IP restriction (если возможно)
- ✅ НЕ давай Withdraw permission
- ✅ Начинай с TESTNET
- ✅ Мониторь каждый день

### **РИСКИ:**

- API ключи могут быть украдены
- Бот может сделать убыточные сделки
- Рынок может резко упасть
- **НАЧИНАЙ С МИНИМУМА!**

---

## 🎯 **ПРОВЕРОЧНЫЙ СПИСОК:**

### **До запуска:**

- [ ] ByBit аккаунт создан
- [ ] KYC верификация пройдена
- [ ] Есть баланс USDT ($20+ для старта)
- [ ] API ключи созданы
- [ ] Ключи добавлены в .env
- [ ] Бот перезапущен
- [ ] Логи показывают "Balance: $XXX"

### **После запуска:**

- [ ] Telegram уведомления приходят
- [ ] Первая сделка (виртуальная) сделана
- [ ] Win rate > 50% за 2-3 дня
- [ ] Готов к LIVE режиму

---

## 📱 **TELEGRAM УВЕДОМЛЕНИЯ:**

После добавления ключей, бот будет слать:

```
🤖 ByBit Bot:

🚀 Trading Bot Started
Mode: TESTNET
Balance: $100,000 USDT
Strategy: RSI + Moving Average

---

📊 Market Analysis:
TON/USDT: $2.45
RSI: 32 (OVERSOLD)
Signal: BUY

---

🟢 OPENED POSITION
Symbol: TONUSDT
Entry: $2.4500
Quantity: 816.33 TON
Amount: $2,000.00
Stop-Loss: $2.3975
Take-Profit: $2.5480
```

**Каждая сделка → уведомление!**

---

## 🚀 **ИТОГО:**

**СЕЙЧАС:**

1. Получи ByBit API ключи (5 минут)
2. Добавь в .env
3. Перезапусти: `pm2 restart crypto-bot`
4. Жди уведомления в Telegram!

**ПОТОМ (2-3 дня):**
5. Тестируй на TESTNET
6. Проверяй результаты
7. Когда уверен → LIVE mode
8. Начинай с $20-30!

---

**❓ ВОПРОСЫ?**

- Hummingbot уже запущен → может там ключи?
- Telegram Wallet → баланс есть?
- ByBit аккаунт → зарегистрирован?

**Пиши! Помогу настроить!** 🔧
