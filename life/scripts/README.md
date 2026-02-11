# Scripts

Эта папка содержит скрипты для работы с бэкапами Singularity.

## Скрипты

### extract_singularity_data.py

Извлекает проекты и задачи из бэкапа Singularity в форматы JSON и Markdown.

**Использование:**
```bash
python3 scripts/extract_singularity_data.py [опции]
```

**Основные параметры:**
- `[backup_file]` - путь к файлу бэкапа (по умолчанию: `data/singularity_backup_2026-02-11.json`)
- `--status {all,complete,incomplete}` - фильтр по статусу выполнения (по умолчанию: `all`)
- `--include-basket` / `--no-include-basket` - включать/исключать задачи из корзины
- `--basket-only` - только задачи из корзины
- `--json-output` - путь к выходному JSON файлу (по умолчанию: `extracted_data.json`)
- `--md-output` - путь к выходному Markdown файлу (по умолчанию: `extracted_data.md`)

**Примеры:**
```bash
# Все задачи
python3 scripts/extract_singularity_data.py

# Только активные не выполненные задачи
python3 scripts/extract_singularity_data.py --status incomplete --no-include-basket

# Только задачи из корзины
python3 scripts/extract_singularity_data.py --basket-only
```

## Документация

- `extract_singularity_data_README.md` - полное руководство по скрипту
- `singularity_backup_analysis.md` - анализ структуры бэкапа Singularity
