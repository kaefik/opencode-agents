# Execution Guide — {Project Name}
Generated: {YYYY-MM-DD}

<!--
ИНСТРУКЦИЯ: Заполни все секции перед запуском task-executor.
Этот файл вставляется verbatim в начало каждого LLM-промпта.
Чем точнее — тем лучше код на выходе.
-->

## Project Context

{1–2 абзаца: что строим, для кого, ключевые ограничения и цели.
Пример: "REST API для системы управления задачами. Многопользовательский режим
с ролями admin/user. MVP: создание/управление задачами, назначение исполнителей,
уведомления по email при изменении статуса."}

## Tech Stack

- Language: TypeScript (ESM, Node 20+)
- Framework: {Hono / Express / Fastify / NestJS / ...}
- DB: {PostgreSQL + drizzle-orm / MySQL + prisma / MongoDB + mongoose / ...}
- Auth: {JWT (access 15m + refresh 7d) / Session / OAuth2}
- Validation: {zod / joi / class-validator}
- Testing: {Vitest + Supertest / Jest + Supertest / ...}
- Logging: {pino / winston / bunyan}
- Metrics: {Prometheus + prom-client / Datadog / ...}
- Package manager: {pnpm / npm / yarn / bun}

## Execution Style

execution_style: careful
# careful  = шаг за шагом, подтверждение перед каждой задачей, много проверок
# aggressive = максимальная скорость, авто-переход к следующей, минимум вопросов

## Code Conventions

### Именование
- Переменные и функции: camelCase
- Классы и интерфейсы: PascalCase
- Файлы: kebab-case.ts
- Константы: UPPER_SNAKE_CASE
- БД-поля: snake_case

### Файловая структура
```
src/
├── routes/         ← роуты (по ресурсам)
├── services/       ← бизнес-логика
├── db/
│   ├── schema/     ← drizzle схемы
│   └── migrations/ ← миграции
├── middleware/     ← auth, validation, error handler
├── lib/            ← утилиты, хелперы
└── types/          ← TypeScript типы
```

### Импорты
- Всегда именованные: `import { foo } from './bar'`
- Никаких default export для сервисов и роутов
- Абсолютные пути через tsconfig paths: `@/services/user`

### Прочее
- ESM only: `"type": "module"` в package.json, никаких `require()`
- Async/await везде, никаких .then()
- Explicit return types на публичных функциях

## Output Format Rules (для LLM)

- **ВСЕГДА возвращай полные файлы** — никаких diff, никакого "остальное остаётся прежним"
- **ВСЕГДА включай все импорты** в начале каждого файла
- **НИКАКИХ TODO** и FIXME комментариев
- **НИКАКИХ placeholder** вида `// implement this later`
- Следовать точно **Output** и **Done when** из карточки задачи
- Если нужен env var которого нет — добавь в .env.example с комментарием

## Error Handling Convention

HTTP коды:
- 400 Bad Request — неверный формат запроса
- 401 Unauthorized — нет или невалидный токен
- 403 Forbidden — нет прав на действие
- 404 Not Found — ресурс не найден
- 409 Conflict — конфликт (дублирование email и т.д.)
- 422 Unprocessable Entity — ошибки валидации
- 500 Internal Server Error — неожиданная ошибка

Формат ответа ошибки:
```json
{
  "error": "Human-readable message",
  "code": "MACHINE_READABLE_CODE",
  "fields": { "email": "Already exists" }  // только для 422
}
```

## Observability Convention

- **Logging:** pino, структурированный JSON
  - Каждый запрос: method, path, status, duration_ms, user_id (если авторизован)
  - Каждая ошибка: error message, stack (только в dev), correlation_id
  - Бизнес-события: `logger.info({ event: 'task.created', task_id, user_id })`

- **Correlation ID:** генерировать UUID per-request, добавлять в response header `X-Correlation-Id`

- **Metrics:** Prometheus counters/histograms
  - `http_requests_total{method,path,status}`
  - `http_request_duration_seconds{method,path}`
  - Ключевые бизнес-метрики: `tasks_created_total`, etc.

## Environment Variables

| Переменная | Описание | Пример |
|-----------|----------|--------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/myapp` |
| `JWT_SECRET` | Секрет для access токенов | 64-char random string |
| `JWT_REFRESH_SECRET` | Секрет для refresh токенов | 64-char random string |
| `PORT` | HTTP порт (default: 3000) | `3000` |
| `LOG_LEVEL` | Уровень логирования | `info` / `debug` |
| `NODE_ENV` | Окружение | `development` / `production` |
