# 📧 Настройка Gmail API для AI Bot

## Шаг 1: Создание Google Cloud Project

1. Открой [Google Cloud Console](https://console.cloud.google.com/)
2. Нажми на выпадающий список проектов вверху слева
3. Нажми **"New Project"** (Создать проект)
4. Введи имя: `Unified-System-Bot`
5. Нажми **Create**

## Шаг 2: Включение Gmail API

1. В боковом меню выбери **APIs & Services** → **Library**
2. В поиске введи `Gmail API`
3. Нажми на **Gmail API**
4. Нажми **ENABLE** (Включить)

## Шаг 3: Настройка OAuth Consent Screen

1. Перейди в **APIs & Services** → **OAuth consent screen**
2. Выбери **External** (если нет организации)
3. Нажми **Create**
4. Заполни:
   - App name: `Gonya Bot`
   - User support email: твой email
   - Developer contact: твой email
5. Нажми **Save and Continue**
6. На странице **Scopes** нажми **Add or Remove Scopes**
7. Найди и добавь:
   - `https://www.googleapis.com/auth/gmail.readonly`
8. Нажми **Update**, затем **Save and Continue**
9. На странице **Test users** нажми **Add Users**
10. Добавь свой Gmail адрес
11. Нажми **Save and Continue**

## Шаг 4: Создание OAuth Credentials

1. Перейди в **APIs & Services** → **Credentials**
2. Нажми **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `Gonya Bot Desktop`
5. Нажми **Create**
6. **ВАЖНО!** Скачай JSON файл нажав **DOWNLOAD JSON**
7. Переименуй файл в `gmail_credentials.json`

## Шаг 5: Размещение файла

Положи `gmail_credentials.json` в одну из папок:

- MacBook: `/Users/macbook/Documents/Unified_System/Windows_AI_Core/config/`
- Server: `/home/gonya/Documents/Unified_System/Windows_AI_Core/config/`

## Шаг 6: Первый запуск (OAuth Flow)

При первом использовании Gmail откроется браузер для авторизации.
После авторизации создастся файл `gmail_token.pickle`.

---

## Краткая инструкция (5 минут)

```bash
1. console.cloud.google.com → New Project → "Unified-System-Bot"
2. APIs & Services → Library → Gmail API → Enable
3. OAuth consent screen → External → Create → Gonya Bot
4. Scopes → gmail.readonly → Save
5. Test users → Add your email → Save
6. Credentials → Create → OAuth client ID → Desktop app
7. Download JSON → gmail_credentials.json
8. Положить в Windows_AI_Core/config/
```

---

**После выполнения:** Скопируй `gmail_credentials.json` в нужную папку и напиши мне — я активирую Gmail модуль!
