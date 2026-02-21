# AGENTS.md

## 1. Описание проекта

### Что это
**Superpowers** — система workflow для разработки ПО, используемая агентами-кодировщиками (Claude Code, OpenCode, Codex, Cursor). Построена на наборе компонуемых "скиллов" (skills) и начальных инструкций.

### Зачем это
- Автоматизирует дисциплину разработки: TDD, дебаггинг, code review
- Гарантирует систематический подход вместо ad-hoc решений
- Позволяет агентам работать автономно часами, следуя плану
- Обеспечивает качество через проверенные workflow

### Архитектура
```
.opencode/
├── superpowers/           # Основные скиллы
│   └── skills/            # Директория скиллов
│       ├── brainstorming/ # Уточнение требований
│       ├── writing-plans/ # Создание планов
│       ├── test-driven-development/
│       ├── systematic-debugging/
│       └── ...            # Другие скиллы
├── skills/                # Пользовательские скиллы
└── plugins/               # Плагины
```

---

## 2. Правила проекта

### Обязательные workflow (срабатывают автоматически)

| Триггер | Скилл | Действие |
|---------|-------|----------|
| Начало разработки | brainstorming | Уточнить требования, создать дизайн |
| Есть дизайн | writing-plans | Создать план реализации |
| Есть план | subagent-driven-development | Запустить субагентов |
| Реализация | test-driven-development | RED-GREEN-REFACTOR цикл |
| Между задачами | requesting-code-review | Ревью кода |
| Завершение | finishing-a-development-branch | Merge/PR/cleanup |

### Стиль кода

**Markdown (SKILL.md):**
- YAML frontmatter: только `name` и `description` (макс 1024 символа)
- `name`: буквы, цифры, дефисы (без скобок, спецсимволов)
- `description`: начинается с "Use when...", third-person, только триггеры (НЕ summary workflow)

```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions]
---
```

**Flowcharts:**
- Только для неочевидных decision points
- Использовать graphviz dot syntax
- НЕ использовать для: reference material, code examples, linear instructions

**Код examples:**
- Один отличный пример > много mediocre
- Полностью runnable
- Комменты объясняют WHY, не WHAT
- Inline для <50 строк, отдельный файл для >50

### Git conventions
- Fork → Branch → PR workflow
- Каждый скилл в отдельной ветке
- Тестирование скиллов через subagents перед merge

---

## 3. Ограничения проекта

### Критические (НЕ нарушать)

**TDD для скиллов:**
```
NO SKILL WITHOUT A FAILING TEST FIRST
```
- Сначала создать pressure scenario без скилла
- Зафиксировать baseline behavior (verbatm rationalizations)
- Написать скилл
- Проверить compliance с скиллом
- Закрыть loopholes

**Запрещено:**
- Создавать несколько скиллов в batch без тестирования каждого
- Редактировать скилл без повторного тестирования
- Держать untested код как "reference"

### CSO (Claude Search Optimization)

**Description field:**
- МАКС 500 символов (желательно)
- Только triggering conditions
- НЕ summary workflow (Claude может follow description вместо skill body)

```yaml
# ❌ BAD: Summary workflow
description: Use for TDD - write test first, watch it fail...

# ✅ GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

### Token limits

| Тип скилла | Лимит слов |
|------------|------------|
| getting-started workflows | <150 |
| Frequently-loaded skills | <200 |
| Other skills | <500 |

### Файловая структура

**Запрещено:**
- Скиллы вне namespace (все в `skills/`)
- Narrative storytelling в SKILL.md
- Multi-language examples (один отличный пример достаточно)
- Generic labels в flowcharts (helper1, step2)

**Обязательно:**
- Flat namespace (все скиллы в одной директории)
- Отдельные файлы только для: heavy reference (100+ lines), reusable tools

### Кросс-ссылки

```markdown
# ✅ GOOD
**REQUIRED BACKGROUND:** Use superpowers:test-driven-development

# ❌ BAD (force-loads, burns context)
@skills/testing/test-driven-development/SKILL.md
```

---

## Команды

### Установка/обновление плагина
```bash
# OpenCode
/opencode plugin install superpowers

# Обновление
/opencode plugin update superpowers
```

### Проверка установки
- Запросить что-то, что триггерит скилл
- Агент должен автоматически invoke relevant skill

### Тестирование скиллов
```bash
# Рендер flowcharts
./render-graphs.js ../some-skill
./render-graphs.js ../some-skill --combine
```

---

## Philosophy

- **Test-Driven Development** — тесты сначала, всегда
- **Systematic over ad-hoc** — процесс вместо угадывания
- **Complexity reduction** — простота как главная цель
- **Evidence over claims** — verify перед success claims

---

## Контакты

- **Issues:** https://github.com/obra/superpowers/issues
- **Marketplace:** https://github.com/obra/superpowers-marketplace
- **Sponsorship:** https://github.com/sponsors/obra
