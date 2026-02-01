# 🚀 ЗАПУСК CRYPTO TRADING BOT

## ✅ **ГОТОВО К ЗАПУСКУ!**

### **Что создано:**

1. **bybit_trading_bot.py** - Полноценный trading bot
   - ✅ ByBit API integration
   - ✅ RSI + Moving Average strategy
   - ✅ Stop-loss -2%, Take-profit +4%
   - ✅ Max 3% на сделку
   - ✅ Telegram уведомления

2. **TESTNET MODE** - Безопасное тестирование
   - Виртуальные деньги
   - Реальный рынок
   - Нет риска

---

## 🔐 **НАСТРОЙКА API КЛЮЧЕЙ:**

### **Шаг 1: Получи ByBit API Keys**

1. Зайди на <https://www.bybit.com/app/user/api-management>
2. Create New Key → API Transaction
3. Permissions:
   - ✅ Read
   - ✅ Trade (Spot)
   - ❌ Withdraw (НЕ ВКЛЮЧАЙ!)

4. Скопируй:
   - API Key: `xxxxxxxxxxxx`
   - API Secret: `yyyyyyyyyyy`

### **Шаг 2: Добавь в .env**

```bash
ssh unified-home-core-cloud
nano /home/gonya/Unified_System_Core/Projects/AI_Core/.env
```

Добавь:

```bash
# ByBit Trading
BYBIT_API_KEY=твой_api_key
BYBIT_API_SECRET=твой_api_secret
ADMIN_CHAT_ID=708531393
```

---

## 🧪 **ТЕСТОВЫЙ ЗАПУСК (TESTNET):**

```bash
ssh unified-home-core-cloud
cd /home/gonya/Unified_System_Core/Projects/AI_Core

# Тест (виртуальные деньги!)
python3 src/bybit_trading_bot.py

# Если работает → запуск в фоне
pm2 start src/bybit_trading_bot.py --name crypto-bot \
  --interpreter python3 \
  --restart-delay=5000

# Мониторинг
pm2 logs crypto-bot
```

**Бот будет торговать виртуальными деньгами на TESTNET!**

---

## ⚠️ **ПЕРЕХОД НА LIVE (РЕАЛЬНЫЕ ДЕНЬГИ):**

**ТОЛЬКО ПОСЛЕ ТЕСТИРОВАНИЯ!**

1. Убедись что бот работает неделю на testnet
2. Проверь статистику (win rate > 55%)
3. Измени в коде:

   ```python
   testnet=False  # Line 265
   ```

---

## 💰 **TELEGRAM WALLET:**

### **Как подключить:**

1. Открой @wallet в Telegram
2. Получи адрес TON
3. Переведи туда "мелочь"

**Бот будет следить за ценой TON и торговать!**

---

## 📊 **СТРАТЕГИЯ:**

### **RSI + Moving Average:**

**ПОКУПКА когда:**

- RSI < 35 (перепродано)
- Цена ниже 30-дневной MA
- = Вероятность роста

**ПРОДАЖА когда:**

- RSI > 65 (перекуплено)
- Цена выше 30-дневной MA
- = Вероятность падения

**Защита:**

- Stop-loss: -2% (выход при убытке)
- Take-profit: +4% (фиксация прибыли)
- Max 5 сделок/день

---

## 📈 **ПРОГНОЗ:**

### **При $50 стартовом капитале:**

**Консервативный:**

- +2-4% в неделю
- = +$1-2/неделя
- За 2 недели: +$2-4

**Оптимистичный:**

- +5-10% в неделю
- = +$2.5-5/неделя
- За 2 недели: +$5-10

**НО! Может быть -5 до -20% если рынок падает!**

---

## 🎯 **РЕКОМЕНДАЦИИ:**

1. **Начни с TESTNET** - 1 неделю
2. **Проверь win rate** - должен быть >50%
3. **Начни с малого** - $20-50 max
4. **Не жди чудес** - это не x100, это +2-5%
5. **Мониторь каждый день** - через Telegram

---

## ✅ **ГОТОВ ЗАПУСТИТЬ?**

```bash
# 1. Установи зависимости
ssh unified-home-core-cloud
cd /home/gonya/Unified_System_Core/Projects/AI_Core
pip install pybit aiohttp

# 2. Тестовый запуск (без API ключей = TESTNET)
python3 src/bybit_trading_bot.py

# 3. Когда получишь ключи → добавь в .env
# 4. Запусти через PM2
pm2 start src/bybit_trading_bot.py --name crypto-bot --interpreter python3
```

**Бот будет слать уведомления в Telegram о каждой сделке!** 📲

---

**ВАЖНО:** Это рискованно! Начни с минимума!
