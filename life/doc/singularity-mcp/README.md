# Singularity MCP для OpenCode - Пакет установки

Полный набор инструкций и скриптов для интеграции SingularityApp с OpenCode через Model Context Protocol.

## 📦 Содержимое пакета

### Инструкции
- **`singularity-opencode-setup.md`** - Подробная инструкция с пошаговым описанием
- **`singularity-opencode-quickstart.md`** - Краткая инструкция для быстрой настройки

### Файлы конфигурации
- **`opencode.json`** - Готовая конфигурация OpenCode для MCP
- **`AGENTS.md`** - Промпт-инструкции для AI ассистента

### Скрипты
- **`install-singularity-mcp.sh`** - Автоматический установщик (Linux/Mac)

## 🚀 Быстрый старт

### Автоматическая установка (рекомендуется)

```bash
# 1. Скачайте скрипт
wget https://path-to-your-files/install-singularity-mcp.sh

# 2. Сделайте его исполняемым
chmod +x install-singularity-mcp.sh

# 3. Запустите установку
./install-singularity-mcp.sh
```

Скрипт автоматически:
- ✅ Скачает и распакует MCP-сервер
- ✅ Установит зависимости
- ✅ Создаст конфигурацию OpenCode
- ✅ Настроит промпт-инструкции
- ✅ Сохранит API токен безопасно

### Ручная установка

Следуйте инструкциям в:
- **Подробная версия:** `singularity-opencode-setup.md`
- **Быстрая версия:** `singularity-opencode-quickstart.md`

## 📋 Что нужно перед началом

1. ✅ Установленный [OpenCode](https://opencode.ai)
2. ✅ Аккаунт в [SingularityApp](https://singularity-app.com)
3. ✅ API токен от SingularityApp
4. ✅ Node.js (для запуска MCP-сервера)

## 🔑 Получение API токена

1. Войдите в [SingularityApp](https://me.singularity-app.com/)
2. Перейдите в **API Access**
3. Создайте новый токен с правами:
   - Создание задач и проектов
   - Редактирование задач и проектов
   - Удаление задач и проектов (опционально)

## 📖 Использование

После установки вы можете управлять задачами через OpenCode:

```bash
# Интерактивный режим
opencode

# Или прямые команды
opencode "Create a task 'Buy groceries' for tomorrow at 10 AM"
opencode "Show my tasks for this week"
opencode "Create a project 'Personal' with emoji 🏠"
```

## 🛠️ Диагностика

### Проверка статуса MCP

```bash
opencode mcp list
```

### Тестирование подключения

```bash
opencode "Create a test task using singularity"
```

## 📂 Структура файлов после установки

```
ваш-проект/
├── .opencode/
│   └── mcp/
│       └── singularity-mcp-server/
│           ├── mcp.js          # Точка входа MCP
│           ├── manifest.json   # Метаданные
│           └── ...
├── opencode.json              # Конфигурация OpenCode
├── AGENTS.md                  # Промпт для AI
└── .env                       # API токен (не коммитить!)
```

## ⚙️ Настройка часового пояса

По умолчанию используется GMT+3. Измените в файле `AGENTS.md`:

```markdown
## Time Zone Configuration
- Use GMT+5 time zone  <!-- Ваш часовой пояс -->
```

Популярные часовые пояса:
- Москва, Минск: `GMT+3`
- Алматы: `GMT+5`
- Владивосток: `GMT+10`
- Екатеринбург: `GMT+5`

## 🔒 Безопасность

⚠️ **Важно:**
- Не коммитьте файл `.env` в Git
- Храните API токен в безопасном месте
- Используйте переменные окружения для токена

Добавьте в `.gitignore`:
```
.env
opencode.json
```

## 🐛 Частые проблемы

### "Connection closed"
- Проверьте правильность API токена
- Убедитесь, что токен установлен в переменной окружения

### Инструменты не появляются
- Перезапустите OpenCode
- Проверьте, что `enabled: true` в конфигурации

### Токен не работает
- Проверьте права доступа в SingularityApp
- Создайте новый токен

Полное руководство по решению проблем: см. `singularity-opencode-setup.md`

## 📚 Дополнительные ресурсы

- [Документация OpenCode](https://opencode.ai/docs/)
- [Документация MCP](https://opencode.ai/docs/mcp-servers/)
- [SingularityApp](https://singularity-app.com)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🤝 Поддержка

Если возникли вопросы:
1. Проверьте раздел "Диагностика проблем" в `singularity-opencode-setup.md`
2. Посетите [Discord сообщество OpenCode](https://opencode.ai/discord)
3. Обратитесь в поддержку SingularityApp

## 📝 Лицензия

MIT License - свободно используйте и распространяйте

---

**Версия:** 1.0  
**Дата:** Февраль 2026  
**Совместимость:** OpenCode 1.0+, Singularity MCP Server 2.1.1

## 🌟 Благодарности

- Команде OpenCode за отличный инструмент
- Команде SingularityApp за MCP-сервер
- Anthropic за Model Context Protocol
