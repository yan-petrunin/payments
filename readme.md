# Асинхронный сервис процессинга платежей

Сервис обработки платежей на FastAPI + RabbitMQ

## Стек

- **FastAPI** — основной фреймворк
- **RabbitMQ** — брокер сообщений
- **PostgreSQL** — хранение ссылок и статистики
- **SQLAlchemy (async)** — работа с БД
- **Alembic** — миграции
- **Poetry** — управление зависимостями
- **Docker / docker-compose** — запуск окружения

---

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/payments` | Обработать платеж |
| `GET` | `/api/v1/payments/{payment_id}` | Получить информацию о платеже |
---
### Тело запроса

| Поле | Тип | Описание |
|------|-----|----------|
| `sum` | `float` | Сумма покупки |
| `currency` | `string` | Валюта (`RUB`, `USD`, `EUR`) |
| `description` | `string` | Описание платежа |
| `metadata` | `object` | Произвольные метаданные |
| `webhook_url` | `string` | URL для получения уведомлений |

**Пример:**
```json
{
  "sum": 1500.00,
  "currency": "RUB",
  "description": "Оплата заказа #42",
  "metadata": { "order_id": 42, "user_id": 7 },
  "webhook_url": "https://example.com/webhook"
}
```

---

### Статусы платежей
| Поле |  Описание |
|------|----------|
| `pending` |  Обрабатывается |
| `succeeded` | Успешно обработан (90% шанс)  |
| `failed` |  Ошибка обработки (10% шанс) |

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo_url>
cd <repo_name>
```

### 2. Создать `.env` файл

```bash
cp .env.example .env
```

Заполнить `.env`, например:

```env
DB_USER=postgres            # имя пользователя базы данных PostgreSQL
DB_PASSWORD=postgres        # пароль пользователя базы данных PostgreSQL
DB_HOST=db                  # хост (по умолчанию db) 
DB_PORT=5432                # порт (по умолчанию 5432)
DB_NAME=postgres            # наименование базы данных PostgreSQL

RABBITMQ_USER=admin         # имя пользователя брокера RabbitMQ
RABBITMQ_PASSWORD=admin     # пароль брокера RabbitMQ
RABBITMQ_HOST=rabbitmq      # хост (rabbitmq по умолчанию)
RABBITMQ_PORT=5672          # порт (5672 по умолчанию)


API_KEY=static_token        # статический токен авторизации
```

### 3. Запустить через docker-compose

```bash
docker-compose up -d --build
```

Сервис будет доступен на `http://localhost:7893`

Swagger UI доступен на `http://localhost:7893/docs`


### 4. Примеры работы
<details>
<summary>POST /api/v1/payments — неавторизованный пользователь</summary>

**Request**
```bash
curl -X 'POST' \
  'http://localhost:7893/api/v1/payments' \
  -H 'accept: application/json' \
  -H 'idempotency-key: 3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'Content-Type: application/json' \
  -d '{
  "sum": 100,
  "currency": "RUB",
  "description": "Покупка одежды",
  "metadata": {
    "shop": "wildberries",
    "weather": "sunny"
  },
  "webhook_url": "https://wildberries.ru"
}'
```

**Response** `401 Unauthorized`
```json
{
  "detail": "Not authenticated"
}
```

</details>

<details>
<summary>POST /api/v1/payments — ошибка валидации</summary>

**Request**
```bash
curl -X 'POST' \
  'http://localhost:7893/api/v1/payments' \
  -H 'accept: application/json' \
  -H 'idempotency-key: 3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'Content-Type: application/json' \
  -d '{
  "sum": 100,
  "currency": "CNY",
  "description": "Покупка одежды",
  "metadata": {
    "shop": "wildberries",
    "weather": "sunny"
  },
  "webhook_url": "https://wildberries.ru"
}'
```

**Response** `422 Error: Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": [
        "body",
        "currency"
      ],
      "msg": "Input should be 'RUB', 'USD' or 'EUR'",
      "input": "CNY",
      "ctx": {
        "expected": "'RUB', 'USD' or 'EUR'"
      }
    }
  ]
}
```

</details>

<details>
<summary>POST /api/v1/payments — успешный платёж</summary>

**Request**
```bash
curl -X 'POST' \
  'http://localhost:7893/api/v1/payments' \
  -H 'accept: application/json' \
  -H 'idempotency-key: 3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'X-API-Key: ···········' \
  -H 'Content-Type: application/json' \
  -d '{
  "sum": 100,
  "currency": "RUB",
  "description": "Покупка одежды",
  "metadata": {
    "shop": "wildberries",
    "weather": "sunny"
  },
  "webhook_url": "https://wildberries.ru"
}'
```

**Response** `200 Success`
```json
{
  "payment_id": 1,
  "status": "pending",
  "created_at": "2026-04-01T12:52:18.752348"
}
```

</details>

<details>
<summary>POST /api/v1/payments — повторный запрос (идемпотентность)</summary>

**Response** `200 OK`
```json
{
  "payment_id": 1,
  "status": "pending",
  "created_at": "2026-04-01T12:52:18.752348"
}
```

</details>

<details>
<summary>GET /api/v1/payments/{payment_id} — неавторизованный пользователь</summary>

**Request**
```bash
curl -X 'GET' \
  'http://localhost:7893/api/v1/payments/1' \
  -H 'accept: application/json' \
  -H 'X-API-Key: ···········'
```

**Response** `401 Unauthorized`
```json
{
  "detail": "Not authenticated"
}
```

</details>

</details>

<details>
<summary>GET /api/v1/payments/{payment_id} — успешный</summary>

**Request**
```bash
curl -X 'GET' \
  'http://localhost:7893/api/v1/payments/1' \
  -H 'accept: application/json' \
  -H 'X-API-Key: ···········'
```

**Response** `200 Success`
```json
{
  "payment_id": 1,
  "status": "succeeded",
  "created_at": "2026-04-01T12:52:18.752348",
  "sum": 100,
  "currency": "RUB",
  "description": "Покупка одежды",
  "metadata": {
    "shop": "wildberries",
    "weather": "sunny"
  },
  "webhook_url": "https://wildberries.ru",
  "modified_at": "2026-04-01T12:52:20.220865"
}
```

</details>

<details>
<summary>GET /api/v1/payments/{payment_id} — платеж не найден</summary>

**Request**
```bash
curl -X 'GET' \
  'http://localhost:7893/api/v1/payments/4' \
  -H 'accept: application/json' \
  -H 'X-API-Key: ···········'
```

**Response** `400 Bad Request`
```json
{
  "detail": "Payment not found"
}
```

</details>