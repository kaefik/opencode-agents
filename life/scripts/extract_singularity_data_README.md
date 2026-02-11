# Руководство по использованию extract_singularity_data.py

## Обзор

Скрипт `extract_singularity_data.py` извлекает данные из бэкапа Singularity и сохраняет их в JSON и Markdown форматы.

## Статусы задач в Singularity

### Статус выполнения (`checked`)

- **`checked = 0`** - задача не выполнена
- **`checked = 1`** - задача выполнена

Это основное поле, определяющее статус выполнения задачи.

### Статус удаления (`showInBasket`)

- **`showInBasket = True`** - задача находится в корзине (удалена)
- **`showInBasket = False`** (или отсутствует) - задача активна

## Статистика бэкапа

| Категория | Количество | Процент |
|-----------|-------------|----------|
| Всего задач | 3176 | 100% |
| Активные задачи (не в корзине) | 3018 | 95.0% |
| Задачи в корзине (удаленные) | 158 | 5.0% |
| Выполненные (активные) | 1858 | 58.5% |
| Не выполненные (активные) | 1160 | 36.5% |
| Выполненные (в корзине) | 7 | 0.2% |
| Не выполненные (в корзине) | 151 | 4.8% |

## Параметры командной строки

### Обязательные параметры

Нет обязательных параметров. По умолчанию используется файл `data/singularity_backup_2026-02-11.json`.

### Опциональные параметры

#### `[backup_file]`

Путь к файлу бэкапа Singularity.

**По умолчанию:** `data/singularity_backup_2026-02-11.json`

**Пример:**
```bash
python3 extract_singularity_data.py /path/to/backup.json
```

#### `--status {all,complete,incomplete}`

Фильтрация по статусу выполнения задачи.

- **`all`** - все задачи (по умолчанию)
- **`complete`** - только выполненные задачи (checked=1)
- **`incomplete`** - только не выполненные задачи (checked=0)

**Примеры:**
```bash
python3 extract_singularity_data.py --status complete
python3 extract_singularity_data.py --status incomplete
```

#### `--include-basket` / `--no-include-basket`

Включать или исключать задачи из корзины.

- **`--include-basket`** (по умолчанию) - включать задачи из корзины
- **`--no-include-basket`** - исключать задачи из корзины

**Примеры:**
```bash
python3 extract_singularity_data.py --no-include-basket  # только активные
python3 extract_singularity_data.py --include-basket      # все задачи
```

#### `--basket-only`

Только задачи из корзины (удаленные).

Этот параметр автоматически устанавливает `--no-include-basket` для других фильтров.

**Пример:**
```bash
python3 extract_singularity_data.py --basket-only
```

#### `--json-output`

Путь к выходному JSON файлу.

**По умолчанию:** `extracted_data.json`

**Пример:**
```bash
python3 extract_singularity_data.py --json-output output.json
```

#### `--md-output`

Путь к выходному Markdown файлу.

**По умолчанию:** `extracted_data.md`

**Пример:**
```bash
python3 extract_singularity_data.py --md-output output.md
```

## Примеры использования

### Все задачи (включая корзину)

```bash
python3 extract_singularity_data.py
```

**Результат:** 3176 задач

### Только активные задачи (без корзины)

```bash
python3 extract_singularity_data.py --no-include-basket
```

**Результат:** 3018 задач

### Активные не выполненные задачи

```bash
python3 extract_singularity_data.py --no-include-basket --status incomplete
```

**Результат:** 1160 задач

### Активные выполненные задачи

```bash
python3 extract_singularity_data.py --no-include-basket --status complete
```

**Результат:** 1858 задач

### Только задачи из корзины

```bash
python3 extract_singularity_data.py --basket-only
```

**Результат:** 158 задач

### Не выполненные задачи из корзины

```bash
python3 extract_singularity_data.py --basket-only --status incomplete
```

**Результат:** 151 задача

### Комбинации фильтров

```bash
# Все не выполненные задачи (включая корзину)
python3 extract_singularity_data.py --status incomplete

# Только выполненные задачи (без корзины)
python3 extract_singularity_data.py --status complete --no-include-basket

# Сохранение в конкретные файлы
python3 extract_singularity_data.py --no-include-basket --status incomplete \
  --json-output my_tasks.json --md-output my_tasks.md
```

## Структура выходных файлов

### JSON файл

```json
{
  "projects": [...],
  "tasks": [...],
  "export_date": "2026-02-11T12:00:00.000Z",
  "total_tasks": 3176,
  "filter": {
    "status": "incomplete"
  },
  "basket_mode": "exclude"
}
```

### Markdown файл

Содержит:
- Список всех проектов в таблице
- Статистику задач
- Задачи по проектам
- Задачи с заметками
- Задачи с дедлайнами
- Повторяющиеся задачи
- Задачи с напоминаниями

## Структура задачи в выходных данных

```json
{
  "id": "T-xxx-xxx-xxx-xxx-xxxxxxxxxxxx",
  "title": "Название задачи",
  "project_id": "P-xxx-xxx-xxx-xxx-xxxxxxxxxxxx",
  "project_title": "Название проекта",
  "group_id": "Q-xxx-xxx-xxx-xxx-xxxxxxxxxxxx",
  "group_title": "Название группы",
  "parent_id": "T-xxx-xxx-xxx-xxx-xxxxxxxxxxxx",
  "parent_title": "Родительская задача",
  "start": "2025-01-01 10:00",
  "deadline": "2025-01-31 18:00",
  "created_date": "2025-01-01 09:00",
  "time_length": 60,
  "priority": 1,
  "priority_text": "Высокий",
  "checked": 0,
  "deferred": false,
  "use_time": true,
  "note": "Текст заметки",
  "tags": ["тег1", "тег2"],
  "notifies": [60, 30],
  "alarm_notify": false,
  "show_in_basket": false,
  "delete_date": ""
}
```

## Частые сценарии

### Получить список актуальных задач

```bash
python3 extract_singularity_data.py --no-include-basket --status incomplete
```

### Посмотреть историю выполненных задач

```bash
python3 extract_singularity_data.py --no-include-basket --status complete
```

### Удаленные задачи (корзина)

```bash
# Все удаленные задачи
python3 extract_singularity_data.py --basket-only

# Удаленные, но не выполненные
python3 extract_singularity_data.py --basket-only --status incomplete
```

### Полный бэкап

```bash
# Все задачи включая корзину
python3 extract_singularity_data.py

# Или явно указав
python3 extract_singularity_data.py --status all --include-basket
```
