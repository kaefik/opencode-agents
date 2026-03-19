# Workflow Guide v2.1 — LLM-Driven Software Development

> Полная документация по применению воркфлоу для создания и развития программных продуктов с LLM.
> Версия 2.1 — актуальна для всех скиллов из пакета `.opencode/skill/`.

---

## Содержание

1. [Обзор воркфлоу](#1-обзор-воркфлоу)
2. [Полная карта скиллов](#2-полная-карта-скиллов)
3. [Структура проекта](#3-структура-проекта)
4. [Путь A: Новый проект](#4-путь-a-новый-проект)
5. [Путь B: Существующий проект](#5-путь-b-существующий-проект)
6. [Фаза 1: Дизайн](#6-фаза-1-дизайн)
7. [Фаза 2: Планирование](#7-фаза-2-планирование)
8. [Фаза 3: Реализация](#8-фаза-3-реализация)
9. [Фаза 4: Верификация](#9-фаза-4-верификация)
10. [Справочник: формат задачи](#10-справочник-формат-задачи)
11. [Справочник: 00-guide.md](#11-справочник-00-guidemd)
12. [Справочник: Канбан-папки](#12-справочник-канбан-папки)
13. [Справочник: приоритизация](#13-справочник-приоритизация)
14. [Быстрый старт — новый проект](#14-быстрый-старт--новый-проект)
15. [Быстрый старт — существующий проект](#15-быстрый-старт--существующий-проект)
16. [Частые сценарии](#16-частые-сценарии)
17. [Что не стоит делать](#17-что-не-стоит-делать)
18. [Changelog](#18-changelog)

---

## 1. Обзор воркфлоу

Воркфлоу состоит из двух путей входа и четырёх общих фаз.

```
ПУТЬ A: Новый проект               ПУТЬ B: Существующий проект
─────────────────────              ──────────────────────────────
brainstorming-skill                project-onboarding
                                   MODE A (новая фича): 10–20 мин
                                   MODE B (весь проект): 30–60 мин
        │                                    │
        └──────────────┬──────────────────────┘
                       ▼
            ФАЗА 1: ДИЗАЙН
            plan-critic  →  вердикт: APPROVED / CONDITIONAL / NEEDS REVISION
                       │
                       ▼
            ФАЗА 2: ПЛАНИРОВАНИЕ
            design-to-plan  →  tasks/{DATE}/ Kanban (L0–L9)
                       │
                       ▼
            ФАЗА 3: РЕАЛИЗАЦИЯ
            task-executor   →  NEXT → PROMPT → DONE → повтор
            context-bridge  →  _context.json        [опционально]
            session-snapshot → _snapshot-*.md       [при перерывах]
                       │
                       ▼
            ФАЗА 4: ВЕРИФИКАЦИЯ
            qa-checklist    →  docs/CHECKLIST-{DATE}.md
            project-portability → PORT-DOC.md       [опционально]
```

**Пять принципов:**
- Никакого кода до утверждённого дизайна (HARD-GATE в brainstorming-skill)
- Каждая задача атомарна: 1–4 часа, один артефакт, одно done-condition
- Задачи выполняются по `priority_score`, не по номеру слоя
- Физическая папка задачи = её текущий статус (Kanban)
- Все скиллы работают без внешних инструментов — только файлы

---

## 2. Полная карта скиллов

| Скилл | Фаза | Вход | Выход | Обязательно? |
|-------|------|------|-------|-------------|
| `brainstorming-skill` | Дизайн (новый проект) | Идея | `plan/*-design.md` | ✅ для нового |
| `project-onboarding` | Вход (существующий проект) | Кодовая база | `plan/*-as-is.md` + `00-guide.md` | ✅ для существующего |
| `plan-critic` | Дизайн — фильтр качества | `plan/*.md` | `plan/*-critique.md` + вердикт | ✅ Всегда |
| `design-to-plan` | Планирование | `plan/*.md` | `tasks/{DATE}/` Kanban | ✅ Всегда |
| `task-executor` | Реализация — основной цикл | `tasks/{DATE}/` | Код | ✅ Всегда |
| `context-bridge` | Реализация — контекст | `done/` задачи | `_context.json` | 🟡 При >10 задач |
| `session-snapshot` | Реализация — пауза/возобновление | `_progress.json` | `_snapshot-*.md` | 🟡 При перерывах >2ч |
| `qa-checklist` | Верификация | `plan/*.md` + `done/` | `CHECKLIST-*.md` | ✅ Всегда |
| `project-portability` | Верификация / Миграция | Весь проект | `PORT-DOC.md` | 🟢 Опционально |

---

## 3. Структура проекта

```
project/
├── .opencode/
│   └── skill/
│       ├── brainstorming-skill/SKILL.md
│       ├── project-onboarding/SKILL.md       ← вход для существующих проектов
│       │   └── references/
│       │       ├── scan-commands.md           ← bash-команды по платформам
│       │       └── layer-status-guide.md      ← критерии done/partial/missing
│       ├── plan-critic/SKILL.md
│       ├── design-to-plan/SKILL.md
│       │   └── references/
│       │       ├── task-sizing-guide.md
│       │       └── llm-prompt-patterns.md
│       ├── task-executor/SKILL.md
│       │   └── references/
│       │       ├── prompt-patterns.md
│       │       └── status-flow.md
│       ├── context-bridge/SKILL.md
│       ├── session-snapshot/SKILL.md
│       ├── qa-checklist/SKILL.md
│       └── project-portability/SKILL.md
│           └── references/
│               ├── platforms.md
│               └── port-doc-template.md
│
├── plan/
│   ├── {DATE}-{slug}-design.md               ← выход brainstorming-skill
│   ├── {DATE}-{slug}-as-is.md                ← выход project-onboarding (MODE B)
│   └── {DATE}-{slug}-critique.md             ← выход plan-critic
│
├── tasks/
│   └── {DATE}/
│       ├── 00-guide.md                       ← tech stack, conventions, execution_style
│       ├── _progress.json                    ← трекер статусов и метрик
│       ├── _context.json                     ← реестр артефактов (context-bridge)
│       ├── _snapshot-{TIMESTAMP}.md          ← снимки сессий (session-snapshot)
│       ├── backlog/                          ← depends_on не готовы
│       │   ├── L0/ L1/ … L9/
│       ├── ready/                            ← зависимости выполнены
│       ├── in_progress/                      ← максимум 1–2 задачи
│       ├── done/                             ← завершённые
│       └── blocked/                          ← ждут внешнего разблокирования
│
└── docs/
    ├── CHECKLIST-{DATE}.md                   ← выход qa-checklist
    └── PORT-DOC.md                           ← выход project-portability
```

---

## 4. Путь A: Новый проект

```
brainstorming-skill
        ↓
plan-critic  (1–2 прохода)
        ↓
design-to-plan
        ↓
task-executor  [+ context-bridge, session-snapshot]
        ↓
qa-checklist
```

Подробно каждая фаза — в разделах 6–9.
Быстрый старт — раздел 14.

---

## 5. Путь B: Существующий проект

Стандартный воркфлоу предполагает старт с нуля. Для существующего проекта нужен другой вход: **`project-onboarding`** — он реверс-инжинирит кодовую базу в документы, совместимые с остальными скиллами.

### Два режима

**MODE A — добавить новую фичу** (10–20 мин)

Стек уже выбран, L0 уже сделан. Нужно добавить конкретную фичу.

```
1. "Используй project-onboarding, MODE A"
   → Сканирует стек, существующие модели, auth-паттерн
   → Заполняет tasks/{DATE}/00-guide.md
   → Выставляет L{N}_status для каждого слоя

2. "Используй brainstorming-skill для [описание новой фичи]"
   → Работает в рамках существующего стека
   → HARD-GATE: только дизайн новой фичи, не переписывает существующее

3. plan-critic → design-to-plan → task-executor
   → design-to-plan читает L{N}_status, пропускает уже готовые слои
   → task-executor стартует с реального состояния
```

**MODE B — полный аудит** (30–60 мин)

Хочешь понять состояние проекта, найти технический долг, выстроить план.

```
1. "Используй project-onboarding, MODE B"
   → Полный реверс-инжиниринг: сущности, фичи, флоу, интеграции
   → Gap-анализ: что есть / чего нет / что сломано
   → Выход: plan/{DATE}-{slug}-as-is.md + 00-guide.md с L{N}_status

2. "Используй plan-critic для plan/{DATE}-as-is.md
    Это существующий проект, фокус на техническом долге"
   → Режим аудита: ранжирует долг и риски
   → Рекомендует: стабилизировать сначала или строить поверх

3. design-to-plan
   → Читает L{N}_status, помечает выполненные слои в _progress.json
   → Генерирует задачи только на пробелы и новые фичи
```

### Поле `L{N}_status` в `00-guide.md`

```markdown
## Existing Layer Status
L0_status: done       # Foundation complete
L1_status: partial    # Users table есть, Products нет
L2_status: partial    # UserService done, ProductService нет
L3_status: partial    # /auth routes ready, /products нет
L4_status: done       # JWT implemented
L5_status: missing    # Нет внешних интеграций
L6_status: partial    # Валидация непоследовательна
L7_status: partial    # 38% coverage, E2E отсутствуют
L8_status: missing    # Нет README и API docs
L9_status: missing    # Только console.log — критический пробел
```

| Статус | Значение |
|--------|----------|
| `done` | Слой полностью реализован и работает |
| `partial` | Частично — чего-то не хватает |
| `missing` | Не реализован |

Критерии оценки каждого слоя: `.opencode/skill/project-onboarding/references/layer-status-guide.md`

### Типичные сценарии

| Ситуация | Режим | Путь |
|----------|-------|------|
| Добавить оплату Stripe | A | onboarding → brainstorming (Stripe) → задачи L5/L6/L7 |
| Проект в хаосе | B | onboarding → plan-critic (аудит) → задачи на долг по приоритету |
| Новый разработчик | B | onboarding → `as-is.md` как документация проекта |
| Проект наполовину переписан | B | onboarding → gap-анализ → задачи только на пробелы |

Быстрый старт — раздел 15.

---

## 6. Фаза 1: Дизайн

### 6.1 Brainstorming Skill (для нового проекта)

**Цель:** превратить идею в утверждённый дизайн-документ.

```
"Используй brainstorming-skill для [описание проекта]"
```

Процесс:
1. LLM изучает контекст (существующие файлы, если есть)
2. Задаёт уточняющие вопросы по одному
3. Предлагает 2–3 архитектурных подхода с trade-offs
4. Представляет дизайн по секциям, получает одобрение после каждой
5. Записывает в `plan/{DATE}-{slug}-design.md`

**HARD-GATE:** никакого кода до явного одобрения дизайна.

---

### 6.2 Plan Critic

**Цель:** найти дыры до декомпозиции.

```
"Используй plan-critic для plan/{DATE}-{slug}-design.md"
```

**Для нового проекта** — ищет дыры в задуманном:
- 5 линз: полнота / согласованность / допущения / YAGNI / осуществимость
- Инверсия 3 ключевых допущений
- Список пропущенных сценариев

**Для существующего проекта** — режим аудита технического долга:
```
"Используй plan-critic для plan/{DATE}-as-is.md
 Это существующий проект, фокус на техническом долге"
```

**Вердикты:**

| Вердикт | Значение | Действие |
|---------|----------|----------|
| `✅ APPROVED` | Всё ок | Переходи к Design-to-Plan |
| `🟡 CONDITIONAL` | Есть блокеры | Исправь, затем продолжай |
| `🔴 NEEDS REVISION` | Нужна переработка | Вернись к Brainstorming / Onboarding |

**Сколько раз:** 1–2. Критика ради критики замедляет.

Выход: `plan/{DATE}-{slug}-critique.md`

---

## 7. Фаза 2: Планирование

### 7.1 Design to Plan

**Цель:** превратить дизайн в атомарные задачи с приоритетами.

```
"Используй design-to-plan для plan/{DATE}-{slug}-design.md"
```

Процесс:
1. Парсит дизайн: сущности, операции, нефункциональные требования
2. Читает `L{N}_status` из `00-guide.md` — пропускает выполненные слои
3. Строит Layer Map (L0–L9)
4. Генерирует атомарные задачи с полями `depends_on`, `impact`, `complexity`, `risk`, `priority_score`
5. Валидирует каждую задачу: атомарность, acceptance criteria, depends_on
6. Генерирует или обновляет `00-guide.md`
7. Записывает задачи в `tasks/{DATE}/backlog/`

**Слои задач:**

| Слой | Что включает |
|------|-------------|
| L0 Foundation | Инициализация, конфиг, CI/CD |
| L1 Data Layer | Схемы, модели, миграции |
| L2 Core Business | Сервисы, доменная логика |
| L3 API/Interface | Роуты, контроллеры, DTO |
| L4 Auth & Security | Аутентификация, middleware |
| L5 Integration | Внешние API, очереди, email |
| L6 Validation & Errors | Валидация, коды ошибок |
| L7 Tests | Unit, integration, e2e |
| L8 Docs & Deploy | README, API docs, деплой |
| L9 Observability | Structured logs, метрики, трейсинг, алерты |

> **L9 не опционален для production.** Для прототипов — можно пропустить с явным обоснованием в `00-guide.md`.

Выход: `tasks/{DATE}/` (Kanban) + `tasks/{DATE}/00-guide.md`

---

### 7.2 Заполни 00-guide.md

После генерации — проверь и дополни все секции (шаблон: `00-guide-TEMPLATE.md`):

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
- Package manager: pnpm

## Execution Style
execution_style: careful
# careful  = шаг за шагом, подтверждение перед каждой задачей
# aggressive = максимальная скорость, авто-переход, минимум вопросов

## Code Conventions
- Именование: camelCase для переменных, PascalCase для классов
- Структура: src/routes, src/services, src/db/schema, src/middleware
- Импорты: именованные, не default export для сервисов
- ESM only, никаких require()

## Output Format Rules (для LLM)
- Всегда полные файлы — никаких diff и "остальное не меняется"
- Всегда все импорты в начале файла
- Никаких TODO и placeholder
- Следовать exact Output и Done-when из карточки задачи

## Error Handling
- Формат: { error: string, code: string }
- HTTP 422 для валидации, 401 для auth, 403 для authz

## Observability Convention
- Логи: pino, structured JSON
- Каждый запрос: method, path, status, duration_ms, user_id
- Correlation ID: UUID per-request в header X-Correlation-Id

## Environment Variables
- DATABASE_URL
- JWT_SECRET / JWT_REFRESH_SECRET
- PORT (default: 3000)
- LOG_LEVEL (default: info)
```

**Правило:** `00-guide.md` вставляется verbatim в начало каждого LLM-промпта. Чем точнее заполнен — тем консистентнее код.

---

## 8. Фаза 3: Реализация

### 8.1 Task Executor — основной цикл

```
NEXT → PROMPT → [выполнение] → DONE → повтор
```

#### MODE: NEXT

```
"следующая задача"
```

1. Читает `00-guide.md` → загружает `execution_style`
2. Находит все задачи в `ready/`
3. Сортирует по `priority_score` убывающе
4. Показывает задачу с наивысшим приоритетом
5. `careful` → спрашивает подтверждение; `aggressive` → сразу генерирует промпт

---

#### MODE: PROMPT

```
"сгенерируй промпт"
```

Структура итогового промпта:
```
=== EXECUTION GUIDE (follow strictly) ===
[полный 00-guide.md — verbatim]

=== CONTEXT FROM COMPLETED TASKS ===
[из _context.json или вставленный вручную]

=== YOUR TASK: [title] (Score: X.X | Effort: M) ===
[полный контент карточки задачи]

=== ACCEPTANCE CRITERIA ===
[из карточки]

=== REMINDER ===
Полные файлы. Все импорты. Никаких TODO.
Следовать Output и Done-when из карточки.
```

Готовый промпт — копируй целиком в Claude Code / Cursor / Copilot.

Файл перемещается: `ready/L[N]/` → `in_progress/L[N]/`

---

#### MODE: DONE

```
"задача готова"
```

1. Запрашивает: что создано (1–2 строки) и содержит ли тесты
2. Перемещает файл: `in_progress/` → `done/`
3. Разблокирует зависимые задачи (перемещает их в `ready/`)
4. Обновляет метрики в `_progress.json`
5. Показывает что разблокировалось с их `priority_score`

---

#### MODE: PROGRESS

```
"покажи прогресс"
```

Выводит:
- Прогресс-бар: X/Y задач (Z%)
- % задач с тестами
- Покрытие по слоям L0–L9
- Списки: DONE / IN PROGRESS / READY по приоритету / BLOCKED

---

#### MODE: BLOCK

```
"задача заблокирована — [причина]"
```

Перемещает в `blocked/`. Автоматически показывает следующую READY задачу.

Когда блокер снят: `"Разблокируй L5/01"`

---

#### MODE: SCAN

```
"пересканируй задачи"
```

Пересинхронизирует `_progress.json` с реальным состоянием папок.
Используй если вручную перемещал файлы.

---

### 8.2 Context Bridge (рекомендуется при >10 задач)

**Проблема:** task-executor каждый раз просит вставить результат предыдущей задачи вручную. При 30+ задачах это превращается в ручной конвейер.

**Решение:** `_context.json` хранит структурированные артефакты каждой выполненной задачи и инжектирует их автоматически.

```
# После каждого DONE:
"запомни результат задачи"
```

Context Bridge запрашивает данные по типу слоя:
- L1 → имена таблиц, поля, constraints, migration path
- L2 → сервисы, методы, сигнатуры
- L3 → эндпоинты, request/response shapes
- L4 → расположение middleware, формат токена
- L9 → библиотека логирования, формат, endpoint метрик

При следующем MODE: PROMPT — автоматически инжектирует блок `=== CONTEXT ===`.

---

### 8.3 Session Snapshot (при перерывах >2 часов)

**Сохранить:**
```
"сохрани сессию"
```
→ `tasks/{DATE}/_snapshot-{TIMESTAMP}.md` — самодостаточный файл со всем состоянием.

**Восстановить:**
```
[вставь содержимое snapshot-файла]
"Вот снэпшот. Прочитай и скажи что следующий шаг."
```

Task Executor автоматически предлагает сохранить snapshot при milestone 25% / 50% / 75%.

---

## 9. Фаза 4: Верификация

### 9.1 QA Checklist

```
"Используй qa-checklist"
```

Процесс:
1. Загружает `plan/*.md` + все задачи из `done/`
2. Строит Feature Inventory — все фичи из дизайна с уровнем риска 🔴🟡🟢
3. **Coverage Gap Report** — каждая фича → задача → DONE?
4. При наличии gaps — показывает список, спрашивает подтверждение
5. Генерирует ручные тест-кейсы (happy path + edge + error)
6. Генерирует спецификации автотестов (unit / integration / e2e)
7. Non-functional checklist: performance, security, observability, data integrity

Выход: `docs/CHECKLIST-{DATE}.md` — включает раздел Sign-off

**Coverage gaps** нужно либо закрыть задачами, либо принять как Known Gap перед релизом.

---

### 9.2 Project Portability (опционально)

```
"Используй project-portability. Целевая платформа: [mobile / CLI / desktop]"
```

Генерирует `PORT-DOC.md` — платформо-нейтральную спецификацию проекта.
Полезно для миграции стека, новой версии продукта или передачи проекта команде.

---

## 10. Справочник: формат задачи

Каждая задача — отдельный `.md` файл. Шаблон (`TASK-TEMPLATE.md` в корне пакета):

```markdown
### L{N}/{NN} — {Task Title}

**Goal:** Одно предложение — что производит этот шаг.
**Input:** Что нужно перед началом.
**Output:** Точный артефакт (имя файла, эндпоинт, схема).
**Done when:** Конкретное, проверяемое условие.
**Acceptance criteria:**
- [ ] Критерий 1
- [ ] Критерий 2
**depends_on:** [L0/01-init-project, L1/02-product-schema]
**impact:** 5        # 1–5: 5 = блокирует всё остальное
**complexity:** 2    # 1–5: 5 = очень сложно
**risk:** 3          # 1–5: 5 = высокий риск блокера
**priority_score:** 6.5  # = (impact × 2 + risk) / complexity
**Est. effort:** M   # XS=30мин, S=1ч, M=2ч, L=4ч
**LLM Prompt Hint:** Конкретная подсказка для LLM.
```

**Именование файлов:**
```
L{слой}/{двузначный_номер}-{kebab-slug}.md

L0/01-init-project.md
L4/01-jwt-middleware.md
L9/01-structured-logging.md
```

**Пример заполненной карточки:**

```markdown
### L4/01 — JWT authentication middleware

**Goal:** Middleware для валидации JWT access-токенов на защищённых роутах.
**Input:** L0/01-init-project.md (DONE), L1/01-user-schema.md (DONE)
**Output:** `src/middleware/auth.middleware.ts`
**Done when:** Middleware отклоняет невалидные токены (401) и инжектирует userId в context.
**Acceptance criteria:**
- [ ] Нет Authorization header → 401 { error: "Unauthorized", code: "NO_TOKEN" }
- [ ] Истёкший токен → 401 { error: "Unauthorized", code: "TOKEN_EXPIRED" }
- [ ] Валидный токен → c.set('user', { id, email, role }) и вызов next()
- [ ] Три unit-теста (Vitest) покрывают все три кейса
**depends_on:** [L0/01-init-project, L1/01-user-schema]
**impact:** 5
**complexity:** 2
**risk:** 4
**priority_score:** 7.0
**Est. effort:** S
**LLM Prompt Hint:** "Hono middleware. Библиотека: jose. HS256, exp 15 мин. Читать из header Authorization: Bearer. Невалидный → { error, code }. Валидный → c.set('user', payload) + next(). Три Vitest unit-теста."
```

---

## 11. Справочник: 00-guide.md

Полный шаблон: `00-guide-TEMPLATE.md` в корне пакета.

**Ключевые секции и их назначение:**

| Секция | Назначение |
|--------|-----------|
| `## Project Context` | 1–2 абзаца: что строим, для кого, ключевые ограничения |
| `## Tech Stack` | Язык, фреймворк, БД, auth, testing, observability, package manager |
| `## Execution Style` | `careful` или `aggressive` — меняет поведение task-executor |
| `## Code Conventions` | Именование, структура папок, стиль импортов |
| `## Output Format Rules` | Правила для LLM: полные файлы, все импорты, никаких TODO |
| `## Error Handling Convention` | Формат ошибок, HTTP-коды |
| `## Observability Convention` | Формат логов, correlation ID, метрики |
| `## Environment Variables` | Список всех env-переменных с описанием |
| `## Existing Layer Status` | `L{N}_status: done/partial/missing` (только для существующих проектов) |

---

## 12. Справочник: Канбан-папки

| Папка | Содержит | Переход — кто и когда |
|-------|----------|----------------------|
| `backlog/` | Задачи, чьи `depends_on` не DONE | Создаётся design-to-plan |
| `ready/` | Все `depends_on` в `done/` | task-executor при DONE зависимости |
| `in_progress/` | Задача взята в работу (макс. 1–2) | task-executor, MODE: PROMPT |
| `done/` | Задача выполнена, артефакт подтверждён | task-executor, MODE: DONE |
| `blocked/` | Ждёт внешнего разблокирования | task-executor, MODE: BLOCK |

**Инварианты:**
- `_progress.json` всегда зеркалит состояние папок
- Рассинхронизация → `"пересканируй задачи"` (MODE: SCAN)
- В `in_progress/` не больше 2 задач одновременно

**Ручное перемещение** (если нужно — после запусти MODE: SCAN):
```bash
# Взять в работу
mv tasks/{DATE}/ready/L2/03-product-service.md tasks/{DATE}/in_progress/L2/

# Завершить
mv tasks/{DATE}/in_progress/L2/03-product-service.md tasks/{DATE}/done/L2/
```

---

## 13. Справочник: приоритизация

### Формула

```
priority_score = (impact × 2 + risk) / complexity
```

| Поле | 1 | 3 | 5 |
|------|---|---|---|
| `impact` | Мелочь | Важная фича | Core — без него не работает |
| `complexity` | Тривиально | Стандартный CRUD | Несколько систем, нетривиальная логика |
| `risk` | Безопасно | Умеренная неопределённость | Высокая вероятность заблокировать всё |

**Примеры:**

| Задача | impact | complexity | risk | score |
|--------|--------|-----------|------|-------|
| JWT middleware | 5 | 2 | 4 | **7.0** |
| User schema | 5 | 2 | 3 | **6.5** |
| Structured logging | 4 | 1 | 4 | **6.0** ← выполняй раньше README |
| README | 2 | 1 | 1 | **2.5** |

**Правило:** `depends_on` приоритетнее score. Задача с score 7.0 остаётся в `backlog/` пока её зависимости не в `done/`.

---

## 14. Быстрый старт — новый проект

**Шаг 1: Дизайн (5–10 мин)**
```
"Используй brainstorming-skill. Я хочу создать [описание]."
```
Отвечай на вопросы, одобряй по секциям → `plan/{DATE}-{slug}-design.md`

**Шаг 2: Критика (2–5 мин)**
```
"Используй plan-critic для plan/{DATE}-{slug}-design.md"
```
Исправь блокеры, получи APPROVED → `plan/{DATE}-{slug}-critique.md`

**Шаг 3: Декомпозиция (3–5 мин)**
```
"Используй design-to-plan для plan/{DATE}-{slug}-design.md"
```
Проверь и дополни `tasks/{DATE}/00-guide.md` → `tasks/{DATE}/` Kanban

**Шаг 4: Выполнение**
```
"следующая задача"
```
Цикл: NEXT → PROMPT → выполни → DONE → повтор.
При перерыве: `"сохрани сессию"`. При >10 задач: подключи context-bridge.

**Шаг 5: Верификация**
```
"Используй qa-checklist"
```
→ `docs/CHECKLIST-{DATE}.md` с Sign-off

---

## 15. Быстрый старт — существующий проект

**Добавить новую фичу (MODE A, ~30 мин)**
```
# 1. Онбординг
"Используй project-onboarding, MODE A"

# 2. Дизайн фичи в контексте существующего стека
"Используй brainstorming-skill для [описание новой фичи]"

# 3. Декомпозиция (L0 и готовые слои пропускаются)
"Используй design-to-plan для plan/{DATE}-{slug}-design.md"

# 4. Выполнение
"следующая задача"

# 5. Верификация
"Используй qa-checklist"
```

**Аудит и план улучшений (MODE B, ~90 мин)**
```
# 1. Полный анализ проекта
"Используй project-onboarding, MODE B"

# 2. Аудит долга
"Используй plan-critic для plan/{DATE}-as-is.md
 Это существующий проект, фокус на техническом долге"

# 3. Задачи только на пробелы
"Используй design-to-plan для plan/{DATE}-as-is.md"

# 4. Выполнение начиная с самого приоритетного долга
"следующая задача"
```

---

## 16. Частые сценарии

**Возобновить работу после перерыва:**
```
# Со снэпшотом:
[вставь _snapshot-*.md]
"Вот снэпшот. Что следующий шаг?"

# Без снэпшота:
"Прочитай tasks/{DATE}/_progress.json, скажи текущее состояние"
```

**Задача слишком большая (effort: L):**
```
"Задача L2/03 слишком большая. Разбей на подшаги."
```
task-executor создаёт `L2/03a`, `L2/03b` в `backlog/`.

**Изменился дизайн в процессе:**
1. Обнови `plan/*-design.md`
2. Запусти plan-critic
3. `"Добавь задачи для изменений в секции [X]"`
4. Обнови `depends_on` у затронутых задач

**Задача заблокирована внешним блокером:**
```
"Задача L5/01 заблокирована — нет SMTP credentials"
# → уходит в blocked/, показывается следующая READY
# Когда блокер снят:
"Разблокируй L5/01"
```

**Что реализовано — текущий статус:**
```
"покажи прогресс"
```

**Понять чужой проект:**
```
"Используй project-onboarding, MODE B"
# → as-is.md как документация + gap-анализ
```

**Портировать на другую платформу:**
```
"Используй project-portability. Целевая платформа: mobile (React Native)"
```

---

## 17. Что не стоит делать

**❌ Не запускай Design-to-Plan без Plan Critic**
Ошибка в дизайне после декомпозиции стоит в 5–10 раз дороже, чем до.

**❌ Не выполняй задачи не по порядку depends_on**
L3 без L2 — код, который не работает, и непонятно почему.

**❌ Не объединяй несколько задач в один промпт**
LLM теряет фокус, acceptance criteria смешиваются.

**❌ Не пропускай 00-guide.md в промптах**
Без него каждый файл будет написан в разном стиле.

**❌ Не добавляй задачи напрямую в `ready/` минуя depends_on**
Нарушает DAG — задача может выполниться до своих зависимостей.

**❌ Не пропускай L9 (Observability) для production**
Без structured logging и метрик невозможно дебажить инциденты.

**❌ Не запускай QA Checklist до завершения всех задач**
Coverage Gap Report будет неполным.

**❌ Не используй MODE B если нужна только новая фича**
MODE B — полный аудит на 30–60 мин. Для добавления фичи достаточно MODE A.

**❌ Не редактируй задачи в `done/` или `in_progress/` вручную**
Это сломает `_progress.json`. Используй MODE: SCAN для пересинхронизации.

---

## 18. Changelog

| Версия | Что изменилось |
|--------|---------------|
| **v2.1** | Скилл `project-onboarding` (MODE A: новая фича / MODE B: аудит), `layer-status-guide.md`, `scan-commands.md` (5 платформ), поле `L{N}_status` в `00-guide.md`, Путь B в документации |
| **v2.0** | Kanban-папки, `priority_score`, Layer 9 Observability, `context-bridge`, `session-snapshot`, `plan-critic`, `qa-checklist`, поля `depends_on / impact / complexity / risk` в задачах |
| **v1.0** | `brainstorming-skill`, `design-to-plan`, `task-executor`, `project-portability` |
