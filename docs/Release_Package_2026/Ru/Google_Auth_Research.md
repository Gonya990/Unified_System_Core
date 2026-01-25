# Исследование: Google Cloud OAuth, Security Bundles, iOS Integration

**Проект:** `gen-lang-client-0982257437`

## 1. Увеличение квоты OAuth (New User Authorization Limit)

**Проблема:** По умолчанию, неверифицированные приложения имеют лимит на количество новых пользователей в день.
**Ссылка (Форма):** [Запрос на увеличение](https://support.google.com/code/contact/oauth_quota_increase)

**Требования для запроса:**

* Вы должны быть **авторизованным разработчиком**.
* Приложение должно пройти настройку **OAuth Consent Screen** (User Type: External vs Internal).
* **Сроки:** Ответ обычно приходит в течение **2-5 рабочих дней**.
* **Процесс:**
    1. Убедитесь, что вы соблюдаете [Application Rate Limits](https://support.google.com/cloud/answer/9028764).
    2. Заполните форму по ссылке выше.
    3. Отслеживайте почту на предмет ответа от Google Trust & Safety.

> [!IMPORTANT]
> Если приложение в режиме "Testing", лимит пользователей — 100. Для увеличения квот необходимо опубликовать приложение в режим "Production" (требуется верификация).

## 2. Security Bundle (Sign In with Google)

**Ссылка:** [Документация Security Bundle](https://developers.google.com/identity/siwg/security-bundle)

**Что это?**
Набор функций, предоставляющих "Сигналы доверия" (Trust Signals) об аккаунте Google, помогающие оценить риски при входе пользователя.

**Ключевые функции:**

1. **Параметр `auth_time`:**
    * **Описание:** Временная метка (Unix seconds), показывающая, *когда именно* пользователь в последний раз вводил пароль или использовал биометрию для входа в Google.
    * **Где находится:** Внутри **ID Token**.
    * **Значение:**
        * **Недавнее:** Указывает на "Свежесть" (активный пользователь). Низкий риск.
        * **Старое:** Указывает на "Стабильность".
    * **Стратегия:** Если `auth_time` очень старое, вы можете запросить повторную аутентификацию (хотя Google не поддерживает принудительный re-auth через API, можно использовать `prompt=login`).
    * **Как запросить:** Добавить `{"auth_time":{"essential":true}}` в параметр `claims` вашего OAuth 2.0 запроса.

## 3. Интеграция с iOS (Google Sign-In)

**Ссылка:** [Начало работы для iOS](https://developers.google.com/identity/sign-in/ios/start-integrating)

**Предварительные требования:**

* Проект в Xcode.
* Bundle ID зарегистрирован в Google Cloud Console.

**Пошаговая реализация:**

### A. Зависимости (Dependencies)

Используйте **CocoaPods** или **Swift Package Manager (SPM)**.

**SPM:**

* Репозиторий: `https://github.com/google/GoogleSignIn-iOS`
* Пакет: `GoogleSignIn` (и `GoogleSignInSwift` для SwiftUI).

### B. Конфигурация (`Info.plist`)

Вам понадобятся два ключа из Cloud Console (OAuth Client -> iOS):

1. **`GIDClientID`**: Ваш OAuth Client ID (для iOS).
2. **`CFBundleURLTypes`**: Кастомная схема URL для callback'а.
    * **Формат:** Перевернутый Client ID (например, `com.googleusercontent.apps.123456...`).

```xml
<key>GIDClientID</key>
<string>YOUR_IOS_CLIENT_ID</string>
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>com.googleusercontent.apps.YOUR_CLIENT_ID_REVERSED</string>
    </array>
  </dict>
</array>
```

### C. Серверная аутентификация (Важно для нас)

Так как у нас есть Python backend (`gen-lang-client`), нам обычно нужен **ID Token** на сервере для валидации.

* **Действие:** Добавьте ключ `GIDServerClientID` в `Info.plist`.
* **Значение:** Client ID вашего **Веб-приложения** (Web Application Client ID), а *не* iOS клиента. Это гарантирует, что токен, выданный iOS приложению, будет валиден для проверки на нашем бэкенде.

```xml
<key>GIDServerClientID</key>
<string>YOUR_WEB_SERVER_CLIENT_ID</string>
```

## Следующие шаги

1. **Квоты:** Если упираемся в лимиты — проверить статус приложения (Testing/Production).
2. **Безопасность:** Включить запрос `auth_time`, если нужна защита от фрода.
3. **iOS:** Убедиться, что в `Info.plist` прописаны оба ID (`GIDClientID` и `GIDServerClientID`).
