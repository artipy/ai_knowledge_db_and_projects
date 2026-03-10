# Практическое задание №8: Вызов функций (Function Calling)

## Цель задания

Освоить механизм function calling в OpenAI API: определение функций, извлечение структурированных данных, параллельный вызов нескольких функций, управление выбором функции и интеграцию с внешними API.

## Связанные материалы

- [[OpenAI_API/Function_Calling|Вызов функций (Function Calling)]]
- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]]
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]]

## Следующие шаги

После выполнения этого задания вы освоили полный стек работы с OpenAI API — от базовых вызовов до function calling и интеграции с внешними сервисами.

## Предварительные требования

- Установленные библиотеки `openai`, `python-dotenv`, `requests`
- Настроенный `.env` файл с API-ключом
- Понимание структур данных Python (словари, списки)
- Базовое знакомство с форматом JSON

---

## Часть 1: Определение функции и извлечение данных (20 минут)

### Задача 1.1: Извлечение информации из резюме

**Исходный текст:**
```
Меня зовут Мария Соколова. Я Frontend-разработчик с 4 годами опыта.
Работаю в Москве, в офисе компании CloudTech. Специализируюсь на React и TypeScript.
Ищу удаленную работу с зарплатой от 200 000 рублей.
```

**Что нужно сделать:**

1. Определите функцию `extract_candidate_info` со следующими параметрами:
   - `name` — полное имя кандидата (строка)
   - `job_title` — желаемая должность (строка)
   - `years_experience` — количество лет опыта (число)
   - `location` — текущий город (строка)
   - `skills` — список ключевых навыков (строка)

2. Отправьте запрос с этим текстом и определённой функцией

3. Извлеките и выведите результат из `tool_calls[0].function.arguments`

**Ожидаемый результат:**
```json
{
  "name": "Мария Соколова",
  "job_title": "Frontend-разработчик",
  "years_experience": 4,
  "location": "Москва",
  "skills": "React, TypeScript"
}
```

**Шаблон кода:**
```python
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_TOKEN"),
    base_url=os.getenv("BASE_URL_GROQ")
)

resume_text = """Меня зовут Мария Соколова..."""

function_definition = [
    {
        'type': 'function',
        'function': {
            'name': 'extract_candidate_info',
            'description': '...',  # Ваше описание
            'parameters': {
                'type': 'object',
                'properties': {
                    # Ваш код здесь
                }
            }
        }
    }
]

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{'role': 'user', 'content': resume_text}],
    tools=function_definition
)

result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## Часть 2: Параллельный вызов нескольких функций (25 минут)

### Задача 2.1: Анализ новостной статьи

**Исходный текст:**
```
Компания Tesla объявила о запуске нового электромобиля Model Q в Берлине, Германия.
Презентация состоялась 15 ноября 2024 года на заводе Gigafactory Berlin.
Илон Маск лично представил модель, назвав её "революцией для массового рынка".
Стартовая цена составит $35,000. Первые поставки запланированы на март 2025 года.
```

**Что нужно сделать:**

1. Определите **две функции** в одном списке `tools`:

   - `extract_event_info` с параметрами:
     - `company` — название компании (строка)
     - `product` — название продукта (строка)
     - `location` — место события (строка)
     - `date` — дата события (строка)

   - `extract_financial_info` с параметрами:
     - `price` — стартовая цена (строка)
     - `currency` — валюта (строка)
     - `delivery_date` — дата первых поставок (строка)

2. Отправьте запрос и выведите результаты обеих функций

3. Проверьте, что `tool_calls` содержит два элемента

**Ожидаемый результат:**
```
=== ИНФОРМАЦИЯ О СОБЫТИИ ===
{"company": "Tesla", "product": "Model Q", "location": "Берлин, Германия", "date": "15 ноября 2024"}

=== ФИНАНСОВАЯ ИНФОРМАЦИЯ ===
{"price": "35000", "currency": "USD", "delivery_date": "март 2025"}

Количество вызванных функций: 2
```

**Шаблон кода:**
```python
article_text = """Компания Tesla объявила..."""

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'extract_event_info',
            'description': '...',
            'parameters': {
                'type': 'object',
                'properties': {
                    # Ваш код здесь
                }
            }
        }
    },
    # Ваш код: вторая функция
]

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{'role': 'user', 'content': article_text}],
    tools=tools
)

tool_calls = response.choices[0].message.tool_calls
print(f"Количество вызванных функций: {len(tool_calls)}")

for call in tool_calls:
    print(f"\n=== {call.function.name.upper()} ===")
    print(call.function.arguments)
```

---

## Часть 3: Управление выбором функции и защита от домыслов (20 минут)

### Задача 3.1: Принудительный выбор функции

Используйте функции из Части 2 (`extract_event_info` и `extract_financial_info`).

**Что нужно сделать:**

1. Отправьте тот же запрос три раза с разными значениями `tool_choice`:
   - `tool_choice='auto'` — модель выбирает сама
   - Принудительно вызвать только `extract_event_info`
   - Принудительно вызвать только `extract_financial_info`

2. Для каждого случая выведите, какие функции были вызваны

**Ожидаемый результат:**
```
=== tool_choice='auto' ===
Вызванные функции: ['extract_event_info', 'extract_financial_info']

=== Принудительно: extract_event_info ===
Вызванные функции: ['extract_event_info']

=== Принудительно: extract_financial_info ===
Вызванные функции: ['extract_financial_info']
```

**Шаблон кода:**
```python
# auto
response_auto = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{'role': 'user', 'content': article_text}],
    tools=tools,
    tool_choice='auto'
)
names_auto = [c.function.name for c in response_auto.choices[0].message.tool_calls]
print(f"=== tool_choice='auto' ===\nВызванные функции: {names_auto}")

# Принудительный вызов конкретной функции
response_forced = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[{'role': 'user', 'content': article_text}],
    tools=tools,
    tool_choice={
        # Ваш код здесь
    }
)
# Вывод результата
```

### Задача 3.2: Защита от домыслов через системное сообщение

**Что нужно сделать:**

1. Отправьте запрос с вопросом `"Какова годовая выручка компании Tesla?"` — информации, которой нет в тексте статьи

2. **Без системного сообщения**: сохраните, что вернёт модель

3. **С системным сообщением** (`"Don't make assumptions..."`) повторите тот же запрос

4. Сравните поведение: получила ли модель данные или сообщила об отсутствии информации?

**Шаблон кода:**
```python
question = "Какова годовая выручка компании Tesla?"

# Без системного сообщения
messages_no_system = [
    {'role': 'user', 'content': question}
]

# С системным сообщением
messages_with_system = [
    {'role': 'system', 'content': "Don't make assumptions about what values to plug into functions. Don't make up values to fill the response with. Ask for clarification if needed"},
    {'role': 'user', 'content': question}
]

for label, msgs in [("Без системного", messages_no_system), ("С системным", messages_with_system)]:
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=msgs,
        tools=tools
    )
    tool_calls = response.choices[0].message.tool_calls
    content = response.choices[0].message.content
    print(f"\n=== {label} сообщением ===")
    print(f"tool_calls: {tool_calls}")
    print(f"content: {content}")
```

---

## Часть 4: Вызов внешнего API (30 минут)

### Задача 4.1: Поисковый чат-бот по книгам

**Что нужно сделать:**

1. Реализуйте функцию `search_books(query)`, которая вызывает бесплатный Open Library API:
   ```
   GET https://openlibrary.org/search.json?q={query}&limit=5
   ```

2. Определите функцию `get_book_recommendations` для передачи в `tools`:
   - Параметр `search_query` — ключевое слово для поиска книг (строка)

3. Настройте системное сообщение: модель — библиотекарь, извлекающий одно ключевое слово из предпочтений пользователя

4. Обработайте ответ: проверьте `finish_reason == 'tool_calls'`, вызовите реальную функцию, выведите список из 5 найденных книг

**Тестовые запросы пользователя:**
- `"Хочу почитать что-нибудь про космос и освоение других планет"`
- `"Посоветуй детективный роман, желательно классику"`

**Ожидаемый результат:**
```
Пользователь: Хочу почитать что-нибудь про космос и освоение других планет

Ключевое слово для поиска: space exploration

Рекомендуемые книги:
1. The Martian
2. Ender's Game
3. A Fire Upon the Deep
4. Seveneves
5. The Case for Mars
```

**Шаблон кода:**
```python
import requests
import json

def search_books(search_query):
    url = 'https://openlibrary.org/search.json'
    params = {'q': search_query, 'limit': 5}
    response = requests.get(url, params=params)
    return response.text

system_prompt = "You are a librarian assistant. Based on user preferences, extract one search keyword to find relevant books."

user_input = "Хочу почитать что-нибудь про космос и освоение других планет"

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_book_recommendations',
            'description': '...',  # Ваше описание
            'parameters': {
                'type': 'object',
                'properties': {
                    'search_query': {
                        # Ваш код здесь
                    }
                }
            }
        }
    }
]

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_input}
    ],
    tools=tools
)

if response.choices[0].finish_reason == 'tool_calls':
    function_call = response.choices[0].message.tool_calls[0].function
    if function_call.name == 'get_book_recommendations':
        query = json.loads(function_call.arguments)['search_query']
        print(f"Ключевое слово для поиска: {query}")

        books_json = search_books(query)
        books_data = json.loads(books_json)

        print("\nРекомендуемые книги:")
        for i, book in enumerate(books_data.get('docs', [])[:5], 1):
            print(f"{i}. {book.get('title', 'Unknown')}")
    else:
        print("Функция не распознана")
else:
    print("Модель не вызвала функцию:", response.choices[0].message.content)
```

---

## Бонусное задание (необязательно, +20 минут)

### Задача 5: Умный роутер запросов

**Сценарий**: Вы создаёте систему поддержки интернет-магазина. В зависимости от запроса пользователя нужно вызывать разные функции.

**Что нужно сделать:**

1. Определите три функции:
   - `check_order_status` — параметры: `order_id` (строка)
   - `get_product_info` — параметры: `product_name` (строка), `category` (строка)
   - `process_return_request` — параметры: `order_id` (строка), `reason` (строка)

2. Протестируйте систему на следующих запросах:
   - `"Где мой заказ #12345?"`
   - `"Расскажите про беспроводные наушники Sony"`
   - `"Хочу вернуть заказ #67890, товар пришел бракованным"`

3. Для каждого запроса выведите:
   - Какая функция была вызвана
   - Извлечённые параметры

**Ожидаемый результат:**
```
Запрос: "Где мой заказ #12345?"
Функция: check_order_status
Параметры: {"order_id": "12345"}

Запрос: "Расскажите про беспроводные наушники Sony"
Функция: get_product_info
Параметры: {"product_name": "наушники Sony", "category": "электроника"}

Запрос: "Хочу вернуть заказ #67890, товар пришел бракованным"
Функция: process_return_request
Параметры: {"order_id": "67890", "reason": "бракованный товар"}
```

---

## Критерии оценки

| Часть | Баллы | Критерий |
|-------|-------|----------|
| Часть 1 | 20 | Корректное определение функции и извлечение всех полей из резюме |
| Часть 2 | 25 | Определение двух функций, параллельный вызов, обход всех tool_calls |
| Часть 3 | 20 | Демонстрация трёх вариантов tool_choice + сравнение поведения с системным сообщением |
| Часть 4 | 25 | Рабочая интеграция с внешним API, корректная обработка ответа |
| Часть 5 | 10 | Роутинг трёх разных запросов к нужным функциям |
| **Всего** | **100** | |

## Рекомендации по выполнению

1. **Читайте `finish_reason`**: перед обращением к `tool_calls` всегда проверяйте, что `finish_reason == 'tool_calls'`
2. **Используйте `json.loads()`**: аргументы функции возвращаются как строка JSON, не как словарь
3. **Описывайте функции точно**: `description` влияет на то, выберет ли модель функцию — чем точнее, тем лучше
4. **Итерируйте по `tool_calls`**: при параллельном вызове не полагайтесь на фиксированный индекс, проходите по всему списку
5. **Тестируйте граничные случаи**: что произойдёт, если нужной информации нет в тексте?

## Что вы освоите

После выполнения этого задания вы сможете:
- Определять функции с точными схемами параметров и передавать их через `tools`
- Извлекать структурированные данные из неструктурированного текста надёжнее, чем через `json_object`
- Организовывать параллельный вызов нескольких функций в одном запросе
- Управлять выбором функции через `tool_choice`
- Предотвращать домыслы модели с помощью системных сообщений
- Интегрировать OpenAI API с внешними REST API через function calling

---

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Function_Calling|Вызов функций (Function Calling)]]*
