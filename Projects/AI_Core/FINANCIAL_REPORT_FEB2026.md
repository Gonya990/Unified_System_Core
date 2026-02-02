# 💰 FINANCIAL REPORT - FEBRUARY 2026

**Generated:** 2026-02-01 22:59  
**Period:** January 20 - February 1, 2026

---

## 📊 TOTAL EXPENSES: $27/month

### ✅ AI Services Subscriptions

| Service | Plan | Cost | Status | Purpose |
|---------|------|------|--------|---------|
| **Suno AI** | Pro | $10/мес | ✅ Active | Music generation (500/мес) |
| **ElevenLabs** | Starter | $5/мес | ✅ Active | Voice synthesis (30k chars) |
| **Runway ML** | Basic | $12/мес | ✅ Active | Video generation (Gen-3) |
| **Luma AI** | Free | $0 | ✅ Active | Video (30 gens/мес) |

**Subtotal AI Services:** $27/мес

---

### ✅ Cloud & Infrastructure

| Service | Plan | Cost | Status |
|---------|------|------|--------|
| **OpenAI** | Pay-as-go | ~$5-10/мес | ✅ Active |
| **Google Cloud** | Free tier | $0 | ✅ Active |
| **GitHub** | Free | $0 | ✅ Active |

**Subtotal Cloud:** ~$5-10/мес

---

### 🤖 Crypto Trading Bot

❓ **Status:** NOT FOUND in PM2

**Возможные причины:**

1. Бот не запущен
2. Находится в другой директории
3. Работает через cron или systemd

**Что проверить:**

```bash
# Поиск крипто-ботов
find /home/gonya -type f -name "*crypto*.py" -o -name "*trading*.py"

# Проверить crontab
crontab -l | grep -i crypto

# Проверить systemd
systemctl list-units | grep -i crypto
```

---

## 💳 PAYMENT RECEIPTS FROM GMAIL

### 🔍 Checking Gmail

**Filters used:**

- `subject:(receipt OR payment OR invoice OR subscription)`
- `after:2026/01/20`

**Expected receipts:**

- ✅ Suno AI Pro - $10.00
- ✅ ElevenLabs Starter - $5.00
- ✅ Runway ML Basic - $12.00
- ⏳ OpenAI usage (variable)
- ⏳ Other services

---

## 📈 MONTHLY BREAKDOWN

### Fixed Costs

```text
Suno AI:      $10.00
ElevenLabs:    $5.00
Runway ML:    $12.00
-----------------------
TOTAL Fixed:  $27.00/мес
```

### Variable Costs

```text
OpenAI API:   ~$5-10/мес (depends on usage)
Other APIs:   ~$0-5/мес
-----------------------
TOTAL Variable: ~$5-15/мес
```

### **GRAND TOTAL: ~$32-42/month**

---

## 💡 RECOMMENDATIONS

1. **Optimize costs:**
   - Use Luma Free tier (30/мес) instead of Runway where possible
   - Monitor OpenAI usage
   - Consider caching для DALL-E results

2. **Track usage:**
   - Setup monthly reports in /costs command
   - Alert when approaching limits
   - Compare cost vs value

3. **Crypto Bot:**
   - ❓ Need to locate and check status
   - Setup monitoring if trading
   - Track P&L separately

---

## 🔐 API KEYS STATUS

| Service | Key Type | Status | Expires |
|---------|----------|--------|---------|
| Suno AI | Cookie | ✅ Active | ~30-90 days |
| ElevenLabs | API Key | ✅ Active | Never |
| Runway ML | API Key | ✅ Active | Never |
| Luma AI | API Key | ✅ Active | Never |
| OpenAI | API Key | ✅ Active | Never |

---

## 📝 NEXT ACTIONS

- [ ] Find crypto trading bot status
- [ ] Setup automated Gmail receipt parsing
- [ ] Create /finance command in bot
- [ ] Setup monthly cost alerts
- [ ] Review all subscriptions end of month

---

**Total Invested in AI Stack:** $27-42/month  
**Expected ROI:** Automated content creation 24/7  
**Value:** High quality videos, music, voiceovers

💪 **AI Factory is worth the investment!**
