# Команда извлечения данных из бэкапа Singularity

## Новая команда

Команда `extract_singularity_data` доступна через MCP сервер и позволяет извлекать данные из бэкапа Singularity.

## Файлы

- **Скрипт**: `scripts/extract_singularity_data.py` - основной скрипт извлечения данных
- **MCP сервер**: `.opencode/mcp/singularity-backup-server/` - сервер для интеграции с opencode
- **Документация**: 
  - `scripts/extract_singularity_data_README.md` - полное руководство по скрипту
  - `scripts/singularity_backup_analysis.md` - анализ структуры бэкапа
  - `.opencode/mcp/singularity-backup-server/README.md` - документация по MCP команде

## Использование

### Основные команды

```bash
# Все задачи (включая корзину)
extract_singularity_data()

# Только активные задачи (без корзины)
extract_singularity_data(include_basket=false)

# Активные не выполненные задачи
extract_singularity_data(status='incomplete', include_basket=false)

# Активные выполненные задачи
extract_singularity_data(status='complete', include_basket=false)

# Только задачи из корзины
extract_singularity_data(basket_only=true)

# Извлечение из другого файла
extract_singularity_data(backup_file='/path/to/backup.json')

# Задачи на сегодня
extract_singularity_data(date='today')

# Подробный список задач на сегодня
extract_singularity_data(date='today', detailed=True)

# Задачи на конкретную дату
extract_singularity_data(date='2026-02-11')

# Невыполненные задачи на сегодня
extract_singularity_data(date='today', status='incomplete', include_basket=False)
```

## Работа с часовыми поясами

Даты в бэкапе Singularity хранятся в формате UTC. Скрипт автоматически конвертирует их в локальный часовой пояс:

- **2026-02-10T21:00:00.000Z** (UTC) → **2026-02-11 00:00** (UTC+3, Казань)

Это важно при использовании параметра `date` - задача с датой начала `2026-02-10T21:00:00.000Z` будет отображаться как запланированная на **2026-02-11**.

## Выходные файлы

После выполнения команды создаются:
- `extracted_data.json` - полные данные в формате JSON
- `extracted_data.md` - отчет в формате Markdown
