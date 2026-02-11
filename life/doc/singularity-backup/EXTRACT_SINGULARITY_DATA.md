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
```

### Параметры

- `backup_file` - путь к файлу бэкапа (по умолчанию: `data/singularity_backup_2026-02-11.json`)
- `status` - фильтр статуса: `all`, `complete`, `incomplete`
- `include_basket` - включать задачи из корзины (по умолчанию: `true`)
- `basket_only` - только задачи из корзины (по умолчанию: `false`)
- `json_output` - путь к JSON файлу (по умолчанию: `extracted_data.json`)
- `md_output` - путь к Markdown файлу (по умолчанию: `extracted_data.md`)

## Выходные файлы

После выполнения команды создаются:
- `extracted_data.json` - полные данные в формате JSON
- `extracted_data.md` - отчет в формате Markdown
