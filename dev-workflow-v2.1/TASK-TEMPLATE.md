# Шаблон файла задачи

Копируй этот шаблон при создании задач вручную.
Design-to-Plan создаёт файлы автоматически в этом формате.

---

```markdown
### L{N}/{NN} — {Task Title}

**Goal:** Одно предложение — что производит этот шаг.
**Input:** Что нужно перед началом (файлы, данные, выполненные задачи).
**Output:** Точный артефакт (имя файла, эндпоинт, схема и т.д.).
**Done when:** Конкретное, проверяемое условие.
**Acceptance criteria:**
- [ ] Критерий 1
- [ ] Критерий 2
- [ ] Критерий 3
**depends_on:** [L0/01-init-project, L1/02-product-schema]
**impact:** 4          # 1–5 (5=блокирует всё остальное)
**complexity:** 2      # 1–5 (5=очень сложно)
**risk:** 3            # 1–5 (5=высокий риск блокера)
**priority_score:** 5.5  # (impact × 2 + risk) / complexity
**Est. effort:** M     # XS=30мин, S=1ч, M=2ч, L=4ч
**LLM Prompt Hint:** Конкретная подсказка как попросить LLM выполнить задачу эффективно.
```

---

## Правила именования файлов

```
L{слой}/{двузначный_номер}-{kebab-slug}.md

L0/01-init-project.md
L0/02-env-config.md
L1/01-user-schema.md
L1/02-product-schema.md
L2/01-user-service.md
L9/01-structured-logging.md
```

## Слои (L0–L9)

| Слой | Название | Что включает |
|------|----------|-------------|
| L0 | Foundation | Инициализация, конфиг, CI/CD |
| L1 | Data Layer | Схемы, модели, миграции, сидеры |
| L2 | Core Business | Сервисы, доменная логика |
| L3 | API/Interface | Роуты, контроллеры, DTO |
| L4 | Auth & Security | Аутентификация, middleware |
| L5 | Integration | Внешние API, очереди, email |
| L6 | Validation & Errors | Валидация, коды ошибок, logging |
| L7 | Tests | Unit, integration, e2e |
| L8 | Docs & Deploy | README, API docs, деплой |
| L9 | Observability | Structured logs, метрики, трейсинг |

## Калибровка полей

### impact (важность)
- 5 = core feature, без него продукт не работает
- 4 = важная фича, используется в большинстве сценариев
- 3 = средняя ценность, нужна но не критична
- 2 = вспомогательная, улучшает UX
- 1 = мелочь, можно отложить

### complexity (сложность)
- 5 = несколько взаимосвязанных систем, нетривиальная логика
- 4 = сложная логика или интеграция с внешним API
- 3 = стандартный CRUD с бизнес-правилами
- 2 = простой CRUD, шаблонный код
- 1 = конфиг, копипаста, тривиально

### risk (риск)
- 5 = высокая вероятность что заблокирует другие задачи или сломает существующее
- 4 = есть неизвестные, возможны сюрпризы
- 3 = умеренная неопределённость
- 2 = понятная задача, мало неизвестных
- 1 = полностью понятно, безопасно

### priority_score
Формула: `(impact × 2 + risk) / complexity`

Выполняй задачи в порядке убывания score (при условии что depends_on выполнены).

## Пример заполненной задачи

```markdown
### L4/01 — JWT authentication middleware

**Goal:** Реализовать middleware для валидации JWT access-токенов на защищённых роутах.
**Input:** L0/01-init-project.md (DONE), L1/01-user-schema.md (DONE)
**Output:** `src/middleware/auth.middleware.ts`
**Done when:** Middleware отклоняет запросы без валидного токена (401) и инжектирует userId в context.
**Acceptance criteria:**
- [ ] Запрос без Authorization header → 401 { error: "Unauthorized", code: "NO_TOKEN" }
- [ ] Запрос с истёкшим токеном → 401 { error: "Unauthorized", code: "TOKEN_EXPIRED" }
- [ ] Запрос с валидным токеном → context.user = { id, email, role }
- [ ] Unit тест покрывает все три кейса
**depends_on:** [L0/01-init-project, L1/01-user-schema]
**impact:** 5
**complexity:** 2
**risk:** 4
**priority_score:** 7.0
**Est. effort:** S
**LLM Prompt Hint:** "Создай Hono middleware для JWT. Библиотека: jose. Access token: HS256, 15 минут. Читать из header Authorization: Bearer <token>. При невалидном → { error, code }. При валидном → c.set('user', payload) и next(). Покрыть тремя unit тестами (Vitest)."
```
