# Управление своими задачами, проектами, привычками 

При работе с задачами, проектами, привычками и заметками используйте skill `singularity-task`.

## Доступные инструменты

### 1. Singularity MCP Server (`singularity-task`)

Основной сервер для работы с Singularity через API. Позволяет:
- Создавать/обновлять/удалять проекты
- Управлять задачами и подзадачами
- Работать с записными книжками
- Отслеживать привычки
- Управлять заметками и тегами
- Работа с Канбан

**Файл конфигурации:** `.opencode/mcp/singularity-mcp-server/`

### 2. Singularity Backup Server (`singularity-backup`)

Сервер для извлечения данных из бэкапов Singularity. Позволяет:
- Извлекать проекты и задачи из JSON бэкапа
- Фильтровать по статусу выполнения (все/выполненные/не выполненные)
- Управлять включением задач из корзины
- Экспортировать данные в JSON и Markdown форматы

**Документация:** `doc/singularity-backup/EXTRACT_SINGULARITY_DATA.md`
**Скрипты:** `scripts/`
**Файл конфигурации:** `.opencode/mcp/singularity-backup-server/`

## Использование

### Работа с API Singularity

При создании задач, проектов и других операций используйте инструменты MCP сервера `singularity-task`.

### Извлечение данных из бэкапа

Для анализа или отчетов используйте команду:

```bash
# Через скрипт
python3 scripts/extract_singularity_data.py --status incomplete --no-include-basket

# Через MCP сервер (если интегрирован)
/extract_singularity_data --status incomplete --include_basket false
```

## Документация

- `references/user_projects.md` - справочник проектов пользователя
- `doc/singularity-backup/` - документация по извлечению бэкапов
- `scripts/` - скрипты для работы с бэкапами
