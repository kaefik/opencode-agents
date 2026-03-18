# Workflow Guide v2 — LLM-Driven Software Development

> Полная документация по применению воркфлоу для создания программных продуктов с LLM.
> Версия 2.0 — актуальна для всех скиллов из пакета `.opencode/skill/`.

---

## Содержание

1. [Обзор воркфлоу](#1-обзор-воркфлоу)
2. [Структура проекта](#2-структура-проекта)
3. [Скиллы: что делает каждый](#3-скиллы-что-делает-каждый)
4. [Фаза 1: Дизайн](#4-фаза-1-дизайн)
5. [Фаза 2: Планирование](#5-фаза-2-планирование)
6. [Фаза 3: Реализация](#6-фаза-3-реализация)
7. [Фаза 4: Верификация](#7-фаза-4-верификация)
8. [Формат файла задачи](#8-формат-файла-задачи)
9. [Формат 00-guide.md](#9-формат-00-guidemd)
10. [Канбан: папки и правила](#10-канбан-папки-и-правила)
11. [Приоритизация задач](#11-приоритизация-задач)
12. [Быстрый старт (15 минут)](#12-быстрый-старт-15-минут)
13. [Частые сценарии](#13-частые-сценарии)
14. [Что не стоит делать](#14-что-не-стоит-делать)

---

## 1. Обзор воркфлоу

```
ФАЗА 1: ДИЗАЙН
  brainstorming-skill  →  plan/{DATE}-{slug}-design.md
  plan-critic          →  plan/{DATE}-{slug}-critique.md
       ↓ (утверждение)
ФАЗА 2: ПЛАНИРОВАНИЕ
  design-to-plan       →  tasks/{DATE}/ (Kanban + 00-guide.md)
       ↓
ФАЗА 3: РЕАЛИЗАЦИЯ
  task-executor        →  итерации: NEXT → PROMPT → DONE
  context-bridge       →  tasks/{DATE}/_context.json  [опционально]
  session-snapshot     →  tasks/{DATE}/_snapshot-*.md [по необходимости]
       ↓
ФАЗА 4: ВЕРИФИКАЦИЯ
  qa-checklist         →  docs/CHECKLIST-{DATE}.md
```

**Принципы:**
- Никакого кода до утверждённого дизайна (HARD-GATE в brainstorming-skill)
- Каждая задача атомарна: 1–4 часа, один артефакт, одно done-condition
- Задачи выполняются по приоритету, не по номеру слоя
- Физическая папка задачи = её текущий статус (Kanban)
- Все скиллы работают без внешних инструментов — только файлы

---

## 2. Структура проекта

```
project/
├── .opencode/
│   └── skill/
│       ├── brainstorming-skill/SKILL.md
│       ├── plan-critic/SKILL.md
│       ├── design-to-plan/SKILL.md
│       ├── task-executor/SKILL.md
│       ├── context-bridge/SKILL.md       ← опционально
│       ├── session-snapshot/SKILL.md     ← опционально
│       ├── qa-checklist/SKILL.md
│       └── project-portability/SKILL.md  ← опционально
│
├── plan/
│   ├── {DATE}-{slug}-design.md           ← выход brainstorming-skill
│   └── {DATE}-{slug}-critique.md         ← выход plan-critic
│
├── tasks/
│   └── {DATE}/
│       ├── 00-guide.md                   ← tech stack, conventions, execution_style
│       ├── _progress.json                ← трекер (task-executor)
│       ├── _context.json                 ← артефакты (context-bridge)
│       ├── _snapshot-{TS}.md             ← снимки сессий (session-snapshot)
│       ├── backlog/                      ← задачи не готовые к выполнению
│       │   ├── L0/
│       │   ├── L1/
│       │   └── ...
│       ├── ready/                        ← готовые к выполнению
│       ├── in_progress/                  ← в работе
│       ├── done/                         ← выполненные
│       └── blocked/                      ← внешний блокер
│
└── docs/
    ├── CHECKLIST-{DATE}.md               ← выход qa-checklist
    └── PORT-DOC.md                       ← выход project-portability
```

---

## 3. Скиллы: что делает каждый

| Скилл | Фаза | Вход | Выход | Обязательно? |
|-------|------|------|-------|-------------|
| `brainstorming-skill` | Дизайн | Идея проекта | `plan/*-design.md` | ✅ Всегда |
| `plan-critic` | Дизайн | `plan/*-design.md` | `plan/*-critique.md` + вердикт | ✅ Всегда |
| `design-to-plan` | Планирование | `plan/*-design.md` | `tasks/{DATE}/` Kanban | ✅ Всегда |
| `task-executor` | Реализация | `tasks/{DATE}/` | Выполненный код | ✅ Всегда |
| `context-bridge` | Реализация | `done/` задачи | `_context.json` | 🟡 При >10 задач |
| `session-snapshot` | Реализация | `_progress.json` | `_snapshot-*.md` | 🟡 При длинных сессиях |
| `qa-checklist` | Верификация | `plan/*-design.md` + `done/` | `CHECKLIST-*.md` | ✅ Всегда |
| `project-portability` | Верификация | Весь проект | `PORT-DOC.md` | 🟢 Если нужна портируемость |

---

## 4. Фаза 1: Дизайн

### 4.1 Brainstorming Skill

**Цель:** Превратить идею в утверждённый дизайн-документ.

**Запуск:**
```
"Используй brainstorming-skill для [описание проекта]"
```

**Что происходит:**
1. LLM изучает контекст проекта (если есть существующие файлы)
2. Задаёт уточняющие вопросы по одному
3. Предлагает 2–3 архитектурных подхода с trade-offs
4. Представляет дизайн по секциям, получает одобрение после каждой
5. Записывает утверждённый дизайн в `plan/{DATE}-{slug}-design.md`

**HARD-GATE:** LLM не пишет никакого кода до явного одобрения дизайна.

**Выход:** `plan/2025-03-15-my-app-design.md`

---

### 4.2 Plan Critic

**Цель:** Найти дыры в дизайне до декомпозиции, пока исправления дёшевы.

**Запуск (после brainstorming-skill):**
```
"Используй plan-critic для plan/2025-03-15-my-app-design.md"
```

**Что происходит:**
1. Анализ через 5 линз: полнота / согласованность / допущения / YAGNI / осуществимость
2. Инверсия 3 ключевых допущений
3. Список пропущенных сценариев
4. Вердикт: APPROVED / CONDITIONAL / NEEDS REVISION

**Если NEEDS REVISION:** исправь `plan/*-design.md`, запусти plan-critic ещё раз.
**Если CONDITIONAL:** исправь блокеры, продолжай.
**Если APPROVED:** переходи к Design-to-Plan.

**Сколько раз запускать:** 1–2. Не больше — критика ради критики замедляет.

**Выход:** `plan/2025-03-15-my-app-critique.md`

---

## 5. Фаза 2: Планирование

### 5.1 Design to Plan

**Цель:** Превратить дизайн в атомарные задачи с приоритетами.

**Запуск:**
```
"Используй design-to-plan для plan/2025-03-15-my-app-design.md"
```

**Что происходит:**
1. Парсит дизайн: сущности, операции, нефункциональные требования
2. Строит Layer Map (L0–L9)
3. Генерирует атомарные задачи с полями: `depends_on`, `impact`, `complexity`, `risk`, `priority_score`
4. Валидирует каждую задачу: атомарность, acceptance criteria, depends_on
5. Генерирует `00-guide.md` (tech stack, execution_style, конвенции)
6. Записывает всё в `tasks/{DATE}/backlog/`

**Слои задач:**

| Слой | Что включает |
|------|-------------|
| L0 Foundation | Инициализация проекта, конфиг, CI/CD |
| L1 Data Layer | Схемы БД, модели, миграции |
| L2 Core Business | Сервисы, доменная логика |
| L3 API/Interface | Роуты, контроллеры, DTO |
| L4 Auth & Security | Аутентификация, авторизация, middleware |
| L5 Integration | Внешние API, очереди, webhooks |
| L6 Validation & Errors | Валидация, коды ошибок, логирование |
| L7 Tests | Unit, integration, e2e |
| L8 Docs & Deploy | API docs, README, деплой |
| L9 Observability | Structured logs, метрики, трейсинг, алерты |

> **L9 не опционален для production.** Для прототипов — можно пропустить с обоснованием.

**Выход:** `tasks/2025-03-15/` (Kanban) + `00-guide.md`

---

### 5.2 Редактирование 00-guide.md

После генерации — **обязательно проверь и дополни** `00-guide.md`:

```markdown
# Execution Guide — My App
Generated: 2025-03-15

## Project Context
REST API для управления задачами с JWT-аутентификацией.

## Tech Stack
- Language: TypeScript
- Framework: Hono
- DB: PostgreSQL + drizzle-orm
- Auth: JWT (access 15m + refresh 7d)
- Testing: Vitest + Supertest
- Observability: pino (logging), Prometheus (metrics)

## Execution Style
execution_style: careful
# careful = шаг за шагом, проверка каждого результата
# aggressive = максимальная скорость, минимум церемоний

## Code Conventions
- Именование: camelCase для переменных, PascalCase для классов
- Структура: src/routes, src/services, src/db/schema
- Импорты: всегда именованные, не default export для сервисов
- ESM only, никаких require()

## Output Format Rules (для LLM)
- Всегда полные файлы, никаких diff или частичного кода
- Всегда все импорты в начале файла
- Никаких TODO, никаких placeholder
- Следовать exact Output и Done-when из карточки задачи

## Error Handling
- Формат: { error: string, code: string }
- HTTP 422 для валидации, 401 для auth, 403 для authz, 500 для неожиданных

## Environment Variables
- DATABASE_URL
- JWT_SECRET
- JWT_REFRESH_SECRET
- PORT (default: 3000)
```

---

## 6. Фаза 3: Реализация

### 6.1 Task Executor: основной цикл

```
NEXT → PROMPT → [выполнение LLM] → DONE → повтор
```

#### NEXT — следующая задача

```
"следующая задача"
"start next task"
```

Task Executor:
1. Читает `00-guide.md` → загружает `execution_style`
2. Находит все задачи в `ready/`
3. **Сортирует по `priority_score` (убывание)**
4. Показывает задачу с наивысшим приоритетом
5. Если `execution_style: careful` → спрашивает подтверждение
6. Если `execution_style: aggressive` → сразу генерирует промпт

#### PROMPT — промпт для LLM

```
"сгенерируй промпт"
"generate prompt"
```

Промпт содержит:
- Полный контент `00-guide.md` (verbatim, наверху)
- Контекст из выполненных задач (из `_context.json` или вставленный вручную)
- Полный контент карточки задачи
- Acceptance criteria
- Reminder: полные файлы, никаких TODO

Готовый промпт — копируй целиком в Claude Code / Cursor / Copilot.

Файл задачи перемещается: `ready/L[N]/task.md` → `in_progress/L[N]/task.md`

#### DONE — отметить выполненной

```
"задача готова"
"mark done"
```

Task Executor:
1. Спрашивает: что было создано (1–2 строки)
2. Спрашивает: содержит ли задача тесты
3. Перемещает файл: `in_progress/` → `done/`
4. Разблокирует зависимые задачи (перемещает в `ready/`)
5. Обновляет метрики в `_progress.json`
6. Показывает что разблокировалось (с приоритетами)

#### PROGRESS — текущее состояние

```
"покажи прогресс"
"метрики"
```

Показывает:
- % выполненных задач (прогресс-бар)
- % задач с тестами
- Покрытие по слоям (L0–L9)
- Списки: DONE / IN PROGRESS / READY (по приоритету) / BLOCKED

#### BLOCK — внешний блокер

```
"задача заблокирована [причина]"
"block task"
```

Перемещает в `blocked/`. Автоматически показывает следующую READY задачу.

---

### 6.2 Context Bridge (опционально, рекомендуется при >10 задач)

**Проблема без Context Bridge:**
Task Executor каждый раз просит вставить результат предыдущей задачи вручную.

**С Context Bridge:**
Результаты хранятся структурированно и инжектируются автоматически.

**После каждого DONE:**
```
"запомни результат задачи"
```

Context Bridge спрашивает структурированные данные по типу слоя
(для L1 — имена таблиц и поля, для L3 — эндпоинты и DTO, и т.д.)
и записывает в `_context.json`.

**При генерации следующего промпта:**
Context Bridge автоматически инжектирует релевантный контекст.

---

### 6.3 Session Snapshot (при перерывах >2 часов)

**Сохранить перед паузой:**
```
"сохрани сессию"
"save session"
```

Создаёт `tasks/{DATE}/_snapshot-{TIMESTAMP}.md` — самодостаточный файл
со всем состоянием: прогресс, архитектура, артефакты, открытые вопросы.

**Восстановить в новой сессии:**
```
Вставь содержимое snapshot-файла и напиши:
"Вот снэпшот нашей сессии. Прочитай и скажи, что следующий шаг."
```

Или:
```
"Восстанови сессию из tasks/2025-03-15/_snapshot-1200.md"
```

**Автоматические подсказки:**
Task Executor предлагает сохранить снэпшот при milestone 25% / 50% / 75%.

---

## 7. Фаза 4: Верификация

### 7.1 QA Checklist

**Запуск после завершения всех задач:**
```
"Используй qa-checklist"
```

**Что происходит:**
1. Загружает design.md + все задачи из `done/`
2. Строит Feature Inventory (все фичи из дизайна)
3. **Coverage Gap Report**: каждая фича → соответствующая задача → DONE?
4. Если есть gaps → показывает список, спрашивает подтверждение
5. Генерирует ручные тест-кейсы (happy path + edge + error)
6. Генерирует спецификации автотестов (unit / integration / e2e)
7. Добавляет non-functional checklist (performance, security, observability, data integrity)

**Выход:** `docs/CHECKLIST-{DATE}.md` с разделом Sign-off

**Coverage gaps:** задачи без соответствующих фич в дизайне — либо закрыть, либо осознанно принять до релиза.

---

## 8. Формат файла задачи

Каждая задача — отдельный `.md` файл. Формат:

```markdown
### L2/03 — Create ProductService

**Goal:** Реализовать сервисный слой для управления продуктами.
**Input:** L1/02-product-schema.md (DONE), L0/01-init-project.md (DONE)
**Output:** `src/services/product.service.ts`
**Done when:** ProductService экспортирует create, list, findById, update, delete.
**Acceptance criteria:**
- [ ] create() принимает { name, price, stock } возвращает Product
- [ ] list() поддерживает пагинацию (offset, limit)
- [ ] findById() бросает NotFoundError если продукт не найден
- [ ] update() и delete() проверяют владельца
**depends_on:** [L0/01-init-project, L1/02-product-schema]
**impact:** 5
**complexity:** 2
**risk:** 2
**priority_score:** 6.0
**Est. effort:** M
**LLM Prompt Hint:** "Создай ProductService для Hono+drizzle-orm. Таблица products: id(uuid), name, price(decimal), stock(int), user_id(FK→users). Методы: create, list(pagination), findById(throws NotFoundError), update(owner check), delete(owner check). Используй транзакции в update+delete."
```

**Правила именования файлов:**
```
L{слой}/{номер}-{slug}.md
L2/03-product-service.md
L4/01-jwt-middleware.md
L9/01-structured-logging.md
```

---

## 9. Формат 00-guide.md

```markdown
# Execution Guide — {Project Name}
Generated: {DATE}

## Project Context
{1–2 абзаца: что строим, для кого, ключевые ограничения}

## Tech Stack
- Language: TypeScript
- Framework: {Hono / Express / Fastify / ...}
- DB: {PostgreSQL + drizzle-orm / MongoDB + mongoose / ...}
- Auth: {JWT / Session / OAuth}
- Testing: {Vitest / Jest + Supertest}
- Observability: {pino, Prometheus / ...}

## Execution Style
execution_style: careful  # careful | aggressive

## Code Conventions
- {naming convention}
- {file structure}
- {import style}
- {async/await vs promises}

## Output Format Rules (для LLM)
- Всегда полные файлы, никаких diff
- Всегда все импорты
- Никаких TODO, никаких placeholder
- Следовать exact Output и Done-when

## Error Handling Convention
{формат ошибок, HTTP коды}

## Environment Variables
- VAR_NAME — описание
```

---

## 10. Канбан: папки и правила

| Папка | Что там | Кто перемещает |
|-------|---------|----------------|
| `backlog/` | Все задачи при создании | design-to-plan |
| `ready/` | depends_on полностью DONE | task-executor (auto при DONE) |
| `in_progress/` | Задача взята в работу | task-executor (MODE: PROMPT) |
| `done/` | Задача выполнена | task-executor (MODE: DONE) |
| `blocked/` | Внешний блокер | task-executor (MODE: BLOCK) |

**Инварианты:**
- В `in_progress/` максимум 1–2 задачи одновременно
- `_progress.json` всегда зеркалит состояние папок
- При рассинхронизации → запусти `task-executor` MODE: SCAN

**Команды перемещения (bash):**
```bash
# Взять задачу в работу (делает task-executor, но можно вручную)
mv tasks/2025-03-15/ready/L2/03-product-service.md \
   tasks/2025-03-15/in_progress/L2/

# Отметить выполненной
mv tasks/2025-03-15/in_progress/L2/03-product-service.md \
   tasks/2025-03-15/done/L2/
```

---

## 11. Приоритизация задач

### Формула

```
priority_score = (impact × 2 + risk) / complexity
```

**Поля:**

| Поле | Шкала | Значение |
|------|-------|----------|
| `impact` | 1–5 | 5 = core feature, блокирует всё остальное |
| `complexity` | 1–5 | 5 = очень сложно, риск застрять |
| `risk` | 1–5 | 5 = высокая вероятность блокера или регрессии |

**Примеры:**

| Задача | impact | complexity | risk | score |
|--------|--------|-----------|------|-------|
| JWT middleware | 5 | 2 | 4 | **7.0** |
| User schema | 5 | 2 | 3 | **6.5** |
| ProductService | 5 | 2 | 2 | **6.0** |
| README | 2 | 1 | 1 | **2.5** |

**Важно:** `depends_on` всегда приоритетнее score. Задача с score 7.0 не выполняется, пока её depends_on не в `done/`.

---

## 12. Быстрый старт (15 минут)

### Шаг 1: Дизайн (5–10 мин диалога)

```
"Используй brainstorming-skill. Я хочу создать [описание проекта]."
```

→ Отвечай на вопросы, одобри дизайн по секциям.
→ Результат: `plan/{DATE}-{slug}-design.md`

### Шаг 2: Критика (2–5 мин)

```
"Используй plan-critic для plan/{DATE}-{slug}-design.md"
```

→ Исправь блокеры если нашлись, получи APPROVED.

### Шаг 3: Декомпозиция (3–5 мин)

```
"Используй design-to-plan для plan/{DATE}-{slug}-design.md"
```

→ Проверь и дополни `tasks/{DATE}/00-guide.md`.
→ Результат: `tasks/{DATE}/` с Kanban-структурой.

### Шаг 4: Выполнение

```
"следующая задача"
```

→ Цикл: NEXT → PROMPT → выполни → DONE → повтор.
→ При перерыве: `"сохрани сессию"`.
→ При >10 задач: использовать context-bridge.

### Шаг 5: Верификация

```
"Используй qa-checklist"
```

→ Проверь coverage gaps, пройди manual + auto тесты.
→ Результат: `docs/CHECKLIST-{DATE}.md` с Sign-off.

---

## 13. Частые сценарии

### Возобновить работу после перерыва

```
# Вставь последний snapshot-файл в чат, затем:
"Вот снэпшот нашей сессии. Что следующий шаг?"

# Или без snapshot:
"Прочитай tasks/2025-03-15/_progress.json и скажи текущее состояние"
```

### Задача оказалась слишком большой

```
"Задача L2/03 слишком большая. Разбей её на подшаги."
```

task-executor создаёт подзадачи `L2/03a`, `L2/03b` и т.д., помещает их в `backlog/`.

### Изменился дизайн в процессе разработки

1. Обнови `plan/*-design.md`
2. Запусти plan-critic ещё раз
3. Добавь новые задачи в `backlog/` вручную или через:
   ```
   "Добавь задачи для изменений в секции [X] дизайна"
   ```
4. Обнови `depends_on` у задач которые зависят от новых

### Задача заблокирована внешним блокером

```
"Задача L5/01 заблокирована — нет SMTP credentials"
```

Перемещается в `blocked/`. Task Executor показывает следующую READY задачу.
Когда блокер снят:
```
"Разблокируй L5/01"
```

### Нужно проверить что реализовано

```
"покажи прогресс"
```

Показывает метрики: % выполненных, % с тестами, покрытие по слоям.

### Хочу портировать проект на другую платформу

```
"Используй project-portability. Целевая платформа: mobile (React Native)"
```

Генерирует PORT-DOC.md (платформо-нейтральная спека) + TASKS-MOBILE.md.

---

## 14. Что не стоит делать

**❌ Не запускай Design-to-Plan без Plan Critic**
Ошибка в дизайне после декомпозиции стоит в 5–10 раз дороже.

**❌ Не выполняй задачи не по порядку зависимостей**
L3 без L2 — код который не работает и непонятно почему.

**❌ Не объединяй несколько задач в один промпт**
LLM теряет фокус, acceptance criteria смешиваются, проверить "done" становится невозможно.

**❌ Не пропускай `00-guide.md` в промптах**
LLM не знает конвенции — каждый файл будет написан по-разному.

**❌ Не добавляй задачи напрямую в `ready/` минуя `depends_on`**
Нарушает DAG — можно выполнить задачу до её зависимостей.

**❌ Не пропускай Layer 9 (Observability) для production**
Без structured logging и метрик невозможно дебажить production-инциденты.

**❌ Не запускай QA Checklist до завершения всех задач**
Coverage Gap Report будет неполным и вводящим в заблуждение.

---

## Версия и изменения

| Версия | Что изменилось |
|--------|---------------|
| v2.0 | Kanban-папки, приоритизация (priority_score), Layer 9 Observability, context-bridge, session-snapshot, plan-critic, qa-checklist |
| v1.0 | brainstorming-skill, design-to-plan, task-executor, project-portability |
