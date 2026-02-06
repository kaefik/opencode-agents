# Инструкция по подключению Singularity MCP к OpenCode

Эта инструкция поможет вам настроить интеграцию SingularityApp с OpenCode через Model Context Protocol (MCP).

## Предварительные требования

- Установленный [OpenCode](https://opencode.ai)
- Аккаунт в [SingularityApp](https://singularity-app.com)
- Node.js установлен на вашем компьютере

## Шаг 1: Получите API токен от SingularityApp

1. Войдите в свой аккаунт SingularityApp
2. Перейдите в раздел **API Access** (обычно находится в настройках аккаунта)
3. Создайте новый API токен
4. Выберите необходимые права доступа:
   - ✅ Создание задач и проектов
   - ✅ Редактирование задач и проектов
   - ✅ Удаление задач и проектов (опционально)
5. Скопируйте созданный токен (он понадобится в шаге 3)

⚠️ **Важно:** Сохраните токен в безопасном месте. Он показывается только один раз!

## Шаг 2: Скачайте и распакуйте MCP-сервер

1. Скачайте файл `.mcpb` от SingularityApp:

```bash
wget https://me.singularity-app.com/download/singularity-mcp-server-2.1.1.mcpb
```

2. Переименуйте файл в `.zip`:

```bash
mv singularity-mcp-server-2.1.1.mcpb singularity-mcp-server-2.1.1.zip
```

3. Создайте директорию для MCP-серверов в вашем проекте:

```bash
mkdir -p .opencode/mcp
```

4. Распакуйте архив:

```bash
unzip singularity-mcp-server-2.1.1.zip -d .opencode/mcp/singularity-mcp-server
```

5. Установите зависимости (если требуется):

```bash
cd .opencode/mcp/singularity-mcp-server
npm install
cd ../../../
```

## Шаг 3: Настройте переменную окружения

Создайте или отредактируйте файл `.env` в корне вашего проекта:

```bash
# Для Linux/Mac
echo "SINGULARITY_API_TOKEN=ваш-токен-здесь" >> .env

# Или добавьте в ~/.bashrc или ~/.zshrc для глобального использования
echo "export SINGULARITY_API_TOKEN='ваш-токен-здесь'" >> ~/.bashrc
source ~/.bashrc
```

Для Windows (PowerShell):
```powershell
[System.Environment]::SetEnvironmentVariable('SINGULARITY_API_TOKEN', 'ваш-токен-здесь', 'User')
```

⚠️ **Замените** `ваш-токен-здесь` на реальный токен из Шага 1!

## Шаг 4: Настройте OpenCode конфигурацию

Создайте или отредактируйте файл `opencode.json` в корне вашего проекта:

**opencode.json**:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "singularity": {
      "type": "local",
      "command": [
        "node",
        ".opencode/mcp/singularity-mcp-server/mcp.js",
        "--baseUrl",
        "https://api.singularity-app.com",
        "--accessToken",
        "{env:SINGULARITY_API_TOKEN}",
        "-n"
      ],
      "enabled": true,
      "timeout": 10000
    }
  }
}
```

### Альтернатива: Глобальная конфигурация

Если вы хотите использовать Singularity во всех проектах, создайте конфигурацию в:

**Linux/Mac:** `~/.config/opencode/opencode.json`  
**Windows:** `%APPDATA%\opencode\opencode.json`

## Шаг 5: Добавьте промпт-инструкции для AI

Создайте файл `AGENTS.md` в корне вашего проекта со следующим содержимым:

**AGENTS.md**:

```markdown
# Singularity Task Management

When working with tasks, projects, habits, and notebooks, use the `singularity` MCP tools.

## Time Zone Configuration
⚠️ **ВАЖНО:** Замените GMT+3 на ваш часовой пояс!
- Use GMT+3 time zone for all task dates and times
- If time is specified in chat, consider it to be in GMT+3

## Working with Projects

1. When adding tasks to a project, always place the task in the project's base task group, unless explicitly specified which other group to add the task to.

2. Project emoji must be specified as hexadecimal Unicode code without prefix:
   - Format: `"1f49e"` (hexadecimal string)
   - NOT Unicode format: `"U+1F49E"`
   - NOT the emoji itself: `"💞"`
   - Examples:
     - 💞 = `"1f49e"`
     - 🎯 = `"1f3af"`
     - 🚀 = `"1f680"`
     - ⭐️ = `"2b50"`

3. Do not set the `showInBasket` field unless specifically asked.

4. Note content must be in Delta format - pass the operations array directly `[{},...]`, NOT `{"ops":[{},...]}`
   - The last insert inside a Delta must always end with a line break

## Working with Tasks

1. For task date and time, use GMT+3 time zone. If time is specified in chat, consider it GMT+3.

2. Notifications format:
   - `notifies: [60, 15]` - array in minutes, highest to lowest (1 hour and 15 minutes in advance)
   - `notify: 1` - main notification enabled
   - `alarmNotify: true` - alarm enabled (false by default, enable only if explicitly specified)

3. Default task priority is `1`.

4. Time handling:
   - `useTime: false` - start time is just a date without specific hour
   - `useTime: true` - start time is real time in GMT+3

5. Date interpretation:
   - Large difference between `modifiedDate` and `createdDate` indicates task was rescheduled
   - `modifiedDate` is technical field of last change, NOT completion time

## Notebooks and Note-like Entries

1. When asked to create a notebook → create a project with `notebook` attribute
2. When adding items to notebook → create task with `isNote` attribute by default
3. If asked to create a task → create the task
4. To add note to non-notebook project → create task with `isNote` attribute

## Working with Habits

1. Pass habit color as string from acceptable values, NOT color code:
   - Acceptable: `"red"`, `"pink"`, `"purple"`, `"deepPurple"`, `"indigo"`, `"lightBlue"`, `"cyan"`, `"teal"`, `"green"`, `"lightGreen"`, `"lime"`, `"yellow"`, `"amber"`, `"orange"`, `"deepOrange"`, `"brown"`, `"grey"`, `"blueGrey"`

2. Active habits have status `0`. Always create habits with status `0`.
```

### Важно: Настройте ваш часовой пояс!

В файле `AGENTS.md` замените все упоминания `GMT+3` на ваш реальный часовой пояс:

- **Москва, Минск:** GMT+3
- **Киев, София:** GMT+2
- **Алматы, Ташкент:** GMT+5
- **Владивосток:** GMT+10
- **Екатеринбург:** GMT+5
- **Новосибирск:** GMT+7

## Шаг 6: Проверьте установку

1. Запустите или перезапустите OpenCode:

```bash
opencode
```

2. Проверьте список MCP-серверов:

```bash
opencode mcp list
```

Вы должны увидеть `singularity` в списке с статусом "enabled".

3. Проверьте доступные инструменты:

```bash
opencode tools list
```

Вы должны увидеть инструменты с префиксом `singularity_`.

## Шаг 7: Протестируйте работу

Попробуйте создать тестовую задачу через OpenCode:

```bash
opencode "Create a test task in Singularity for tomorrow at 10 AM"
```

Или в интерактивном режиме:

```
Создай задачу "Проверить работу Singularity MCP" на завтра в 10:00
```

## Диагностика проблем

### Ошибка: "Connection closed"

**Решение:**
1. Проверьте, что токен правильно установлен в переменной окружения:
   ```bash
   echo $SINGULARITY_API_TOKEN
   ```

2. Попробуйте запустить сервер вручную:
   ```bash
   cd .opencode/mcp/singularity-mcp-server
   node mcp.js --baseUrl https://api.singularity-app.com --accessToken "ваш-токен" -n
   ```

### Ошибка: "MCP server singularity is not a remote server"

Это нормально, если вы используете локальный MCP-сервер. Игнорируйте это сообщение при выполнении `opencode mcp debug singularity`.

### Инструменты не появляются

**Решение:**
1. Убедитесь, что в `opencode.json` параметр `enabled: true`
2. Перезапустите OpenCode
3. Проверьте логи:
   ```bash
   opencode --verbose
   ```

### Токен не работает

**Решение:**
1. Проверьте права доступа токена в настройках SingularityApp
2. Создайте новый токен с полными правами
3. Обновите переменную окружения

## Структура файлов проекта

После настройки у вас должна быть следующая структура:

```
ваш-проект/
├── .opencode/
│   └── mcp/
│       └── singularity-mcp-server/
│           ├── mcp.js
│           ├── index.js
│           ├── manifest.json
│           └── ... (другие файлы)
├── opencode.json
├── AGENTS.md
└── .env (опционально, если токен здесь)
```

## Дополнительные настройки

### Отключение MCP-сервера временно

В `opencode.json` измените:

```json
{
  "mcp": {
    "singularity": {
      "enabled": false
    }
  }
}
```

### Использование только для конкретного агента

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "singularity": {
      "type": "local",
      "command": ["node", ".opencode/mcp/singularity-mcp-server/mcp.js", "--baseUrl", "https://api.singularity-app.com", "--accessToken", "{env:SINGULARITY_API_TOKEN}", "-n"],
      "enabled": true
    }
  },
  "tools": {
    "singularity_*": false
  },
  "agents": {
    "task-manager": {
      "tools": {
        "singularity_*": true
      }
    }
  }
}
```

Теперь только агент `task-manager` будет иметь доступ к Singularity.

## Полезные ссылки

- [Документация OpenCode](https://opencode.ai/docs/)
- [Документация MCP в OpenCode](https://opencode.ai/docs/mcp-servers/)
- [SingularityApp](https://singularity-app.com)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Поддержка

Если возникли проблемы:
1. Проверьте [документацию OpenCode](https://opencode.ai/docs/troubleshooting/)
2. Задайте вопрос в [Discord сообществе OpenCode](https://opencode.ai/discord)
3. Проверьте настройки API токена в SingularityApp

---

**Версия инструкции:** 1.0  
**Последнее обновление:** февраль 2026  
**Совместимость:** OpenCode 1.0+, Singularity MCP Server 2.1.1
