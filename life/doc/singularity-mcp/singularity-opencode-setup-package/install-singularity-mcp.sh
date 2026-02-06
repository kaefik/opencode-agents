#!/bin/bash

# Singularity MCP Setup Script for OpenCode
# Автоматическая установка и настройка

set -e

echo "🚀 Установка Singularity MCP для OpenCode"
echo "=========================================="
echo ""

# Проверка наличия необходимых инструментов
command -v node >/dev/null 2>&1 || { echo "❌ Node.js не установлен. Установите Node.js и повторите попытку."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm не установлен. Установите npm и повторите попытку."; exit 1; }

# Запрос API токена
echo "📝 Введите ваш Singularity API токен:"
echo "   (Получить можно в https://me.singularity-app.com/ → API Access)"
read -s SINGULARITY_TOKEN

if [ -z "$SINGULARITY_TOKEN" ]; then
    echo "❌ Токен не может быть пустым"
    exit 1
fi

# Запрос часового пояса
echo ""
echo "🌍 Введите ваш часовой пояс (например: GMT+3, GMT+5, GMT-5):"
read TIMEZONE

if [ -z "$TIMEZONE" ]; then
    echo "⚠️  Часовой пояс не указан, используется GMT+3 по умолчанию"
    TIMEZONE="GMT+3"
fi

echo ""
echo "📦 Скачивание MCP-сервера..."

# Скачивание файла
wget -q https://me.singularity-app.com/download/singularity-mcp-server-2.1.1.mcpb || {
    echo "❌ Не удалось скачать MCP-сервер"
    exit 1
}

echo "✅ MCP-сервер скачан"

# Распаковка
echo "📂 Распаковка..."
mv singularity-mcp-server-2.1.1.mcpb singularity-mcp-server-2.1.1.zip
mkdir -p .opencode/mcp
unzip -q singularity-mcp-server-2.1.1.zip -d .opencode/mcp/singularity-mcp-server

echo "✅ MCP-сервер распакован"

# Установка зависимостей
echo "📦 Установка зависимостей..."
cd .opencode/mcp/singularity-mcp-server
npm install --silent
cd ../../..

echo "✅ Зависимости установлены"

# Создание .env файла
echo ""
echo "🔐 Настройка переменных окружения..."
if [ ! -f .env ]; then
    echo "SINGULARITY_API_TOKEN=$SINGULARITY_TOKEN" > .env
    echo "✅ Создан файл .env"
else
    if grep -q "SINGULARITY_API_TOKEN" .env; then
        sed -i "s/SINGULARITY_API_TOKEN=.*/SINGULARITY_API_TOKEN=$SINGULARITY_TOKEN/" .env
        echo "✅ Обновлен токен в .env"
    else
        echo "SINGULARITY_API_TOKEN=$SINGULARITY_TOKEN" >> .env
        echo "✅ Добавлен токен в .env"
    fi
fi

# Создание opencode.json
echo "⚙️  Создание конфигурации OpenCode..."
cat > opencode.json << 'EOF'
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
EOF

echo "✅ Создан файл opencode.json"

# Создание AGENTS.md
echo "📋 Создание инструкций для AI..."
cat > AGENTS.md << EOF
# Singularity Task Management

When working with tasks, projects, habits, and notebooks, use the \`singularity\` MCP tools.

## Time Zone Configuration

- Use $TIMEZONE time zone for all task dates and times
- If time is specified in chat, consider it to be in $TIMEZONE

## Working with Projects

1. When adding tasks to a project, always place the task in the project's base task group, unless explicitly specified which other group to add the task to.

2. Project emoji must be specified as hexadecimal Unicode code without prefix:
   - Format: \`"1f49e"\` (hexadecimal string)
   - NOT Unicode format: \`"U+1F49E"\`
   - NOT the emoji itself: \`"💞"\`
   - Examples:
     - 💞 = \`"1f49e"\`
     - 🎯 = \`"1f3af"\`
     - 🚀 = \`"1f680"\`
     - ⭐️ = \`"2b50"\`

3. Do not set the \`showInBasket\` field unless specifically asked.

4. Note content must be in Delta format - pass the operations array directly \`[{},...]\`, NOT \`{"ops":[{},...]}\`
   - The last insert inside a Delta must always end with a line break

## Working with Tasks

1. For task date and time, use $TIMEZONE time zone. If time is specified in chat, consider it $TIMEZONE.

2. Notifications format:
   - \`notifies: [60, 15]\` - array in minutes, highest to lowest (1 hour and 15 minutes in advance)
   - \`notify: 1\` - main notification enabled
   - \`alarmNotify: true\` - alarm enabled (false by default, enable only if explicitly specified)

3. Default task priority is \`1\`.

4. Time handling:
   - \`useTime: false\` - start time is just a date without specific hour
   - \`useTime: true\` - start time is real time in $TIMEZONE

5. Date interpretation:
   - Large difference between \`modifiedDate\` and \`createdDate\` indicates task was rescheduled
   - \`modifiedDate\` is technical field of last change, NOT completion time

## Notebooks and Note-like Entries

1. When asked to create a notebook → create a project with \`notebook\` attribute
2. When adding items to notebook → create task with \`isNote\` attribute by default
3. If asked to create a task → create the task
4. To add note to non-notebook project → create task with \`isNote\` attribute

## Working with Habits

1. Pass habit color as string from acceptable values, NOT color code:
   - Acceptable: \`"red"\`, \`"pink"\`, \`"purple"\`, \`"deepPurple"\`, \`"indigo"\`, \`"lightBlue"\`, \`"cyan"\`, \`"teal"\`, \`"green"\`, \`"lightGreen"\`, \`"lime"\`, \`"yellow"\`, \`"amber"\`, \`"orange"\`, \`"deepOrange"\`, \`"brown"\`, \`"grey"\`, \`"blueGrey"\`

2. Active habits have status \`0\`. Always create habits with status \`0\`.
EOF

echo "✅ Создан файл AGENTS.md"

# Очистка временных файлов
rm -f singularity-mcp-server-2.1.1.zip

echo ""
echo "✨ Установка завершена успешно!"
echo ""
echo "📋 Следующие шаги:"
echo "   1. Запустите OpenCode: opencode"
echo "   2. Проверьте MCP: opencode mcp list"
echo "   3. Протестируйте: opencode \"Create a test task for tomorrow\""
echo ""
echo "📁 Созданные файлы:"
echo "   - .opencode/mcp/singularity-mcp-server/"
echo "   - opencode.json"
echo "   - AGENTS.md"
echo "   - .env"
echo ""
echo "🎉 Готово! Теперь вы можете управлять задачами через OpenCode!"
