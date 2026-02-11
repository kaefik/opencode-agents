# Singularity Backup Extraction

Документация по работе с бэкапами Singularity.

## Файлы

- [EXTRACT_SINGULARITY_DATA.md](EXTRACT_SINGULARITY_DATA.md) - обзор и использование команды извлечения
- [README.md](../../scripts/README.md) - обзор скриптов в папке `scripts/`
- [singularity_backup_analysis.md](../../scripts/singularity_backup_analysis.md) - анализ структуры бэкапа
- [extract_singularity_data_README.md](../../scripts/extract_singularity_data_README.md) - полное руководство по скрипту

## Использование

```bash
python3 scripts/extract_singularity_data.py [опции]
```

### Основные параметры

- `[backup_file]` - путь к файлу бэкапа (по умолчанию: `data/singularity_backup_2026-02-11.json`)
- `--status {all,complete,incomplete}` - фильтр по статусу выполнения
- `--include-basket` / `--no-include-basket` - включать/исключать задачи из корзины
- `--basket-only` - только задачи из корзины
- `--json-output` - путь к выходному JSON файлу
- `--md-output` - путь к выходному Markdown файлу

### Примеры

```bash
# Все задачи
python3 scripts/extract_singularity_data.py

# Только активные не выполненные задачи
python3 scripts/extract_singularity_data.py --status incomplete --no-include-basket

# Только задачи из корзины
python3 scripts/extract_singularity_data.py --basket-only
```

## Связанные файлы

- `.opencode/mcp/singularity-backup-server/` - MCP сервер для интеграции с opencode
- `AGENTS.md` - общий обзор инструментов Singularity
