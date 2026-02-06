# Быстрая настройка Singularity MCP в OpenCode

## Шаги за 5 минут

### 1. Получите API токен
- Войдите в [SingularityApp](https://me.singularity-app.com/)
- Перейдите в **API Access**
- Создайте токен с правами на создание/редактирование/удаление

### 2. Скачайте и распакуйте MCP-сервер

```bash
# Скачать
wget https://me.singularity-app.com/download/singularity-mcp-server-2.1.1.mcpb

# Переименовать и распаковать
mv singularity-mcp-server-2.1.1.mcpb singularity-mcp-server-2.1.1.zip
mkdir -p .opencode/mcp
unzip singularity-mcp-server-2.1.1.zip -d .opencode/mcp/singularity-mcp-server

# Установить зависимости
cd .opencode/mcp/singularity-mcp-server && npm install && cd ../../../
```

### 3. Настройте токен

```bash
# Linux/Mac
echo "export SINGULARITY_API_TOKEN='ваш-токен'" >> ~/.bashrc
source ~/.bashrc

# Или для проекта
echo "SINGULARITY_API_TOKEN=ваш-токен" >> .env
```

### 4. Создайте opencode.json

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

### 5. Создайте AGENTS.md

```markdown
# Singularity Task Management

When working with tasks, projects, habits, and notebooks, use the `singularity` MCP tools.

## Time Zone: GMT+3
⚠️ Замените на ваш часовой пояс!

## Key Rules

### Projects
- Emoji as hex: `"1f680"` for 🚀
- Notes in Delta format: `[{},...]`
- Default: base task group

### Tasks
- Default priority: `1`
- Notifications: `notifies: [60, 15]`
- `useTime: false` for date-only

### Habits
- Color as string: `"red"`, `"blue"`, etc.
- Active status: `0`

### Notebooks
- Create project with `notebook` attribute
- Items as tasks with `isNote` attribute
```

### 6. Запустите OpenCode

```bash
opencode
```

### 7. Проверьте

```bash
opencode mcp list
opencode "Create a test task for tomorrow at 10 AM using singularity"
```

## Готово! 🎉

Теперь вы можете управлять задачами в SingularityApp через OpenCode.

---

📚 [Полная инструкция](./singularity-opencode-setup.md) | 🔧 [Диагностика проблем](./singularity-opencode-setup.md#диагностика-проблем)
