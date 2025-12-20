# Руководство по удалённому подключению к Windows ПК с Macbook Air M1

## Обзор

Это руководство описывает несколько способов удалённого подключения к Windows ПК с вашего Macbook Air M1 для настройки и работы с ИИ окружением.

---

## Способ 1: Microsoft Remote Desktop (Рекомендуется)

### Преимущества
- ✅ Полноценный графический интерфейс
- ✅ Поддержка копирования/вставки между системами
- ✅ Передача файлов через drag-and-drop
- ✅ Бесплатное приложение от Microsoft
- ✅ Хорошая производительность

### Настройка на Windows ПК

1. **Включите Remote Desktop на Windows:**
   - Откройте **Settings** → **System** → **Remote Desktop**
   - Включите **Enable Remote Desktop**
   - Запомните имя ПК (например, `DESKTOP-ABC123`)

2. **Настройте сетевой доступ:**
   - Убедитесь, что Windows ПК и Mac находятся в одной сети
   - Узнайте IP адрес Windows ПК:
     ```powershell
     ipconfig
     # Найдите IPv4 Address (например, 192.168.1.100)
     ```

3. **Настройте брандмауэр (если нужно):**
   ```powershell
   # Разрешите Remote Desktop через брандмауэр
   Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
   ```

### Установка на Mac

1. **Установите Microsoft Remote Desktop:**
   ```bash
   brew install --cask microsoft-remote-desktop
   ```
   
   Или скачайте из Mac App Store: [Microsoft Remote Desktop](https://apps.apple.com/app/microsoft-remote-desktop/id1295203466)

2. **Настройте подключение:**
   - Запустите **Microsoft Remote Desktop**
   - Нажмите **"+"** → **Add PC**
   - Введите IP адрес Windows ПК (например, `192.168.1.100`)
   - Введите имя пользователя и пароль Windows
   - Сохраните подключение

3. **Подключитесь:**
   - Дважды кликните на сохранённое подключение
   - Примите сертификат безопасности (если запрошено)

### Передача файлов через RDP

1. В настройках подключения в Microsoft Remote Desktop:
   - **Redirection** → **Folders**
   - Добавьте папку `windows-rtx-ai-setup` с вашего Mac
   - Эта папка будет доступна на Windows как сетевой диск

2. На Windows ПК:
   - Откройте **File Explorer**
   - Найдите подключённую папку в **Network locations**
   - Скопируйте файлы на локальный диск Windows

---

## Способ 2: SSH (Для командной строки)

### Преимущества
- ✅ Лёгкий и быстрый
- ✅ Минимальное использование сетевого трафика
- ✅ Идеален для запуска скриптов
- ✅ Безопасное подключение

### Настройка на Windows ПК

1. **Установите OpenSSH Server:**
   ```powershell
   # Запустите PowerShell от имени администратора
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   
   # Запустите службу SSH
   Start-Service sshd
   
   # Настройте автозапуск
   Set-Service -Name sshd -StartupType 'Automatic'
   
   # Разрешите SSH через брандмауэр (обычно делается автоматически)
   New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
   ```

2. **Проверьте IP адрес:**
   ```powershell
   ipconfig
   # Запомните IPv4 адрес
   ```

### Подключение с Mac

1. **Подключитесь через SSH:**
   ```bash
   # Замените username и IP адресом вашего Windows ПК
   ssh username@192.168.1.100
   
   # Введите пароль Windows пользователя
   ```

2. **Копирование файлов на Windows через SCP:**
   ```bash
   # Скопировать всю папку
   scp -r ~/Applications/VSCode/windows-rtx-ai-setup username@192.168.1.100:C:/Users/username/
   
   # Скопировать отдельный файл
   scp setup-rtx-ai-environment.ps1 username@192.168.1.100:C:/Users/username/
   ```

3. **Запуск PowerShell скриптов через SSH:**
   ```bash
   # Подключитесь по SSH
   ssh username@192.168.1.100
   
   # На Windows выполните:
   powershell -ExecutionPolicy Bypass -File C:\Users\username\windows-rtx-ai-setup\setup-rtx-ai-environment.ps1
   ```

### Настройка SSH ключей (опционально, для удобства)

1. **На Mac создайте SSH ключ (если нет):**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Скопируйте ключ на Windows:**
   ```bash
   ssh-copy-id username@192.168.1.100
   ```

3. **Теперь можно подключаться без пароля:**
   ```bash
   ssh username@192.168.1.100
   ```

---

## Способ 3: Visual Studio Code Remote - SSH

### Преимущества
- ✅ Редактируйте файлы на Windows прямо из VS Code на Mac
- ✅ Запускайте терминал Windows в VS Code
- ✅ Отладка и разработка как на локальной машине
- ✅ Полная интеграция с Git

### Настройка

1. **Установите расширение Remote - SSH в VS Code:**
   - Откройте VS Code на Mac
   - Перейдите в Extensions (⌘+Shift+X)
   - Найдите и установите **"Remote - SSH"** от Microsoft

2. **Настройте SSH подключение:**
   - Нажмите **F1** → **Remote-SSH: Connect to Host...**
   - Выберите **"+ Add New SSH Host..."**
   - Введите: `ssh username@192.168.1.100`
   - Выберите файл конфигурации (обычно `~/.ssh/config`)

3. **Подключитесь:**
   - Нажмите **F1** → **Remote-SSH: Connect to Host...**
   - Выберите ваш Windows ПК из списка
   - Откройте папку: `C:\Users\username\windows-rtx-ai-setup`

4. **Работайте с файлами:**
   - Редактируйте PowerShell скрипты
   - Запускайте команды в интегрированном терминале
   - Всё работает так, как будто вы на Windows

---

## Способ 4: Использование облачных сервисов (Альтернатива)

Если прямое подключение невозможно (например, разные сети, нет публичного IP):

### TeamViewer
```bash
# Скачайте на обе системы
# Mac: brew install --cask teamviewer
# Windows: https://www.teamviewer.com/
```

### AnyDesk
```bash
# Mac: brew install --cask anydesk
# Windows: https://anydesk.com/
```

### Tailscale (VPN mesh сеть)
```bash
# Создаёт приватную сеть между устройствами
# Mac: brew install --cask tailscale
# Windows: https://tailscale.com/download/windows
```

---

## Рекомендуемый workflow

### 1. Начальная настройка

```bash
# На Mac: Установите Microsoft Remote Desktop
brew install --cask microsoft-remote-desktop

# Скопируйте файлы на Windows через RDP folder sharing
# или через SCP
scp -r ~/Applications/VSCode/windows-rtx-ai-setup username@windows-ip:C:/Users/username/
```

### 2. Установка компонентов

```bash
# Подключитесь по RDP для графического интерфейса
# Запустите PowerShell от имени администратора
# Выполните:
cd C:\Users\username\windows-rtx-ai-setup
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-rtx-ai-environment.ps1
```

### 3. Разработка и тестирование

```bash
# Используйте VS Code Remote - SSH для:
# - Редактирования кода
# - Запуска скриптов
# - Отладки

# Используйте RDP для:
# - Мониторинга GPU (nvidia-smi)
# - Визуальной отладки
# - Работы с GUI приложениями
```

---

## Устранение проблем

### Не удаётся подключиться по RDP

1. **Проверьте настройки брандмауэра:**
   ```powershell
   # На Windows
   Get-NetFirewallRule -DisplayGroup "Remote Desktop" | Enable-NetFirewallRule
   ```

2. **Убедитесь, что пользователь в группе Remote Desktop Users:**
   ```powershell
   Add-LocalGroupMember -Group "Remote Desktop Users" -Member "username"
   ```

### Не удаётся подключиться по SSH

1. **Проверьте статус службы SSH:**
   ```powershell
   Get-Service sshd
   # Должно быть "Running"
   ```

2. **Проверьте порт:**
   ```powershell
   netstat -an | findstr :22
   ```

### Медленное подключение

1. **Снизьте качество графики в RDP** (в настройках подключения)
2. **Используйте SSH вместо RDP** для скриптов
3. **Сжимайте файлы** перед передачей:
   ```bash
   # На Mac
   tar -czf setup.tar.gz windows-rtx-ai-setup/
   scp setup.tar.gz username@windows-ip:C:/Users/username/
   
   # На Windows
   tar -xzf setup.tar.gz
   ```

---

## Безопасность

### Рекомендации:

1. **Используйте сложные пароли** для Windows учётной записи
2. **Настройте SSH ключи** вместо паролей
3. **Ограничьте доступ по IP** (если возможно):
   ```powershell
   New-NetFirewallRule -DisplayName "RDP from Mac" -Direction Inbound -LocalPort 3389 -Protocol TCP -RemoteAddress 192.168.1.50 -Action Allow
   ```
4. **Используйте VPN** если подключаетесь через интернет
5. **Отключайте Remote Desktop** когда не используете

---

## Полезные команды

### Проверка подключения с Mac

```bash
# Ping Windows ПК
ping 192.168.1.100

# Проверка SSH порта
nc -zv 192.168.1.100 22

# Проверка RDP порта
nc -zv 192.168.1.100 3389

# Trace route
traceroute 192.168.1.100
```

### Мониторинг Windows ПК удалённо

```bash
# Через SSH
ssh username@192.168.1.100 "nvidia-smi"
ssh username@192.168.1.100 "powershell Get-Process | Sort-Object CPU -Descending | Select-Object -First 10"
```

---

## Дополнительные ресурсы

- [Microsoft Remote Desktop Documentation](https://docs.microsoft.com/windows-server/remote/remote-desktop-services/clients/remote-desktop-mac)
- [OpenSSH for Windows](https://docs.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse)
- [VS Code Remote - SSH](https://code.visualstudio.com/docs/remote/ssh)
