# Команда извлечения данных из бэкапа Singularity

## Обзор

Команда `extract_singularity_data` позволяет извлекать проекты и задачи из бэкапа Singularity в форматы JSON и Markdown с поддержкой фильтрации.

## Использование

### Базовое использование

```
/extract_singularity_data
```

Извлекает все задачи из бэкапа по умолчанию (`data/singularity_backup_2026-02-11.json`).

### Параметры

| Параметр | Тип | Описание | По умолчанию |
|----------|-----|----------|--------------|
| `backup_file` | string | Путь к файлу бэкапа Singularity | `data/singularity_backup_2026-02-11.json` |
| `status` | string | Фильтр по статусу выполнения (`all`, `complete`, `incomplete`) | `all` |
| `include_basket` | boolean | Включать задачи из корзины | `true` |
| `basket_only` | boolean | Только задачи из корзины | `false` |
| `json_output` | string | Путь к выходному JSON файлу | `extracted_data.json` |
| `md_output` | string | Путь к выходному Markdown файлу | `extracted_data.md` |

### Примеры

#### Все задачи (включая корзину)
```
/extract_singularity_data
```

#### Только активные задачи (без корзины)
```
/extract_singularity_data --include_basket false
```

#### Активные не выполненные задачи
```
/extract_singularity_data --status incomplete --include_basket false
```

#### Активные выполненные задачи
```
/extract_singularity_data --status complete --include_basket false
```

#### Только задачи из корзины
```
/extract_singularity_data --basket_only true
```

#### Не выполненные задачи из корзины
```
/extract_singularity_data --basket_only true --status incomplete
```

#### Извлечение из другого файла бэкапа
```
/extract_singularity_data --backup_file /path/to/backup.json
```

#### Сохраниение в другие файлы
```
/extract_singularity_data --json_output my_tasks.json --md_output my_tasks.md
```

## Статусы задач в Singularity

### Статус выполнения (`checked`)

- **`checked = 0`** - задача не выполнена
- **`checked = 1`** - задача выполнена

### Статус удаления (`showInBasket`)

- **`showInBasket = True`** - задача находится в корзине (удалена)
- **`showInBasket = False`** (или отсутствует) - задача активна

## Выходные файлы

### JSON файл
Содержит проекты и задачи в формате JSON с полной информацией:
- ID, название, даты, приоритеты
- Связи с проектами, группами, родительскими задачами
- Заметки, теги, напоминания
- Настройки повторения

### Markdown файл
Содержит:
- Список всех проектов в таблице
- Статистику задач
- Задачи по проектам
- Задачи с заметками
- Задачи с дедлайнами
- Повторяющиеся задачи
- Задачи с напоминаниями

## Статистика бэкапа

| Категория | Количество | Процент |
|-----------|-----------|----------|
| Всего задач | 3176 | 100% |
| Активные задачи (не в корзине) | 3018 | 95.0% |
| Задачи в корзине (удаленные) | 158 | 5.0% |
| Выполненные (активные) | 1858 | 58.5% |
| Не выполненные (активные) | 1160 | 36.5% |
| Выполненные (в корзине) | 7 | 0.2% |
| Не выполненные (в корзине) | 151 | 4.8% |

## Частые сценарии

### Получить список актуальных задач
```
/extract_singularity_data --status incomplete --include_basket false
```

### Посмотреть историю выполненных задач
```
/extract_singularity_data --status complete --include_basket false
```

### Удаленные задачи (корзина)
```
# Все удаленные задачи
/extract_singularity_data --basket_only true

# Удаленные, но не выполненные
/extract_singularity_data --basket_only true --status incomplete
```

### Полный бэкап
```
# Все задачи включая корзину
/extract_singularity_data
```
