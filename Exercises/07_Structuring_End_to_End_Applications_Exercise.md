# Практическое задание №7: Структурирование end-to-end приложений

## Цель задания

Научиться строить production-ready код для работы с OpenAI API: получать структурированные JSON-ответы, грамотно обрабатывать ошибки, оптимизировать запросы через батчинг, реализовывать retry-логику и контролировать количество токенов.

## Связанные материалы

- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]]
- [[Python_for_AI/Python_Decorators|Декораторы в Python]]

## Следующие шаги

После выполнения этого задания знания о структурировании API-вызовов можно применить в контексте построения чат-ботов — см. [[Exercises/06_Prompt_Engineering_for_Chatbots_Exercise|Практическое задание №6]].

## Предварительные требования

- Установленные библиотеки: `openai`, `python-dotenv`, `tenacity`, `tiktoken`
- Настроенный `.env` файл с API-ключом
- Пройденные задания №1–2 (базовая работа с OpenAI API)

```bash
pip install openai python-dotenv tenacity tiktoken
```

---

## Часть 1: Структурированный JSON-ответ (20 минут)

### Задача 1.1: Каталог профессий

**Что нужно сделать:**

1. Отправьте запрос к API с параметром `response_format={'type': 'json_object'}`, который вернёт список из **4 IT-профессий** в следующем формате:

```json
[
  {
    "title": "Название должности",
    "description": "Краткое описание (1 предложение)",
    "key_skills": ["навык1", "навык2", "навык3"],
    "avg_salary_usd": 90000
  }
]
```

2. Распарсите полученный JSON и выведите только названия должностей и средние зарплаты в отсортированном по убыванию порядке.

**Ожидаемый результат:**
```
=== IT-ПРОФЕССИИ ПО ЗАРПЛАТЕ ===
1. [Название] — $XXX,XXX
2. [Название] — $XXX,XXX
3. [Название] — $XXX,XXX
4. [Название] — $XXX,XXX
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

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[
        {
            "role": "user",
            "content": # Ваш промпт здесь — обязательно укажите JSON-формат в тексте
        }
    ],
    response_format={"type": "json_object"}
)

raw_json = response.choices[0].message.content

# Ваш код: распарсить JSON и отсортировать по зарплате
data = json.loads(raw_json)
# ...
```

---

### Задача 1.2: Структурированный анализ текста

**Исходный текст:**
```
Компания DataVision открывает вакансию старшего аналитика данных в московском офисе.
Требования: опыт работы от 3 лет, знание Python и SQL обязательно, опыт с Spark будет
плюсом. Зарплата: 180 000 — 220 000 рублей в месяц. Формат работы: гибридный (2 дня в офисе).
Контакт: hr@datavision.ru
```

**Что нужно сделать:**

Создайте промпт, который извлечёт из текста вакансии структурированные данные в JSON:

```json
{
  "company": "...",
  "position": "...",
  "location": "...",
  "experience_years": 3,
  "required_skills": ["..."],
  "optional_skills": ["..."],
  "salary_min": 180000,
  "salary_max": 220000,
  "work_format": "...",
  "contact": "..."
}
```

**Шаблон кода:**
```python
vacancy_text = """..."""

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[
        {
            "role": "user",
            "content": f# Ваш промпт для извлечения данных из текста в JSON-формате
        }
    ],
    response_format={"type": "json_object"}
)

# Ваш код: вывести каждое поле с меткой
result = json.loads(response.choices[0].message.content)
# ...
```

**Ожидаемый результат:**
```
Компания: DataVision
Должность: Старший аналитик данных
Город: Москва
Опыт (лет): 3
Обязательные навыки: Python, SQL
...
```

---

## Часть 2: Обработка ошибок (25 минут)

### Задача 2.1: Классификация ошибок

**Что нужно сделать:**

Реализуйте функцию `safe_request(prompt, api_key=None, role="user")`, которая:

1. Принимает произвольный промпт, опциональный API-ключ и роль сообщения
2. Обрабатывает следующие ошибки по-разному:
   - `openai.AuthenticationError` → выводит `"[AUTH ERROR] Неверный API-ключ."`
   - `openai.RateLimitError` → выводит `"[RATE LIMIT] Превышен лимит запросов. Попробуйте позже."`
   - `openai.BadRequestError` → выводит `"[BAD REQUEST] Некорректный запрос: {детали ошибки}"`
   - `Exception` → выводит `"[ERROR] Неизвестная ошибка: {детали}"`
3. При успехе возвращает текст ответа

Проверьте функцию на **трёх сценариях**:
- Корректный запрос (должен вернуть ответ)
- Неверный API-ключ (`api_key="invalid_key"`)
- Невалидная роль (передайте `role="god"`)

**Шаблон кода:**
```python
import openai

def safe_request(prompt, api_key=None, role="user"):
    _client = OpenAI(
        api_key=api_key or os.getenv("GROQ_TOKEN"),
        base_url=os.getenv("BASE_URL_GROQ")
    )

    try:
        response = _client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[{"role": role, "content": prompt}]
        )
        return response.choices[0].message.content

    except openai.AuthenticationError:
        # Ваш код
        pass
    except openai.RateLimitError:
        # Ваш код
        pass
    except openai.BadRequestError as e:
        # Ваш код
        pass
    except Exception as e:
        # Ваш код
        pass

# Тест 1: корректный запрос
print("--- Тест 1: корректный запрос ---")
result = safe_request("Назови столицу Франции.")
print(result)

# Тест 2: неверный ключ
print("\n--- Тест 2: неверный API-ключ ---")
safe_request("Привет!", api_key="sk-invalid")

# Тест 3: невалидная роль
print("\n--- Тест 3: невалидная роль ---")
safe_request("Привет!", role="god")
```

**Ожидаемый результат:**
```
--- Тест 1: корректный запрос ---
Париж.

--- Тест 2: неверный API-ключ ---
[AUTH ERROR] Неверный API-ключ.

--- Тест 3: невалидная роль ---
[BAD REQUEST] Некорректный запрос: ...
```

---

### Задача 2.2: Обёртка с логированием

**Что нужно сделать:**

Доработайте функцию `safe_request` до `logged_request`, которая дополнительно:

1. До вызова API выводит: `"[LOG] Отправка запроса... (символов в промпте: N)"`
2. После успешного ответа выводит: `"[LOG] Ответ получен. Токенов использовано: N"`
3. При любой ошибке выводит: `"[LOG] Запрос завершился ошибкой."`

**Шаблон кода:**
```python
def logged_request(prompt, role="user"):
    print(f"[LOG] Отправка запроса... (символов в промпте: {len(prompt)})")

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[{"role": role, "content": prompt}]
        )
        # Ваш код: логировать успех и вернуть ответ

    except Exception as e:
        # Ваш код: логировать ошибку и обработать её
        pass

# Проверка
logged_request("Расскажи кратко о Python за 2 предложения.")
```

---

## Часть 3: Батчинг запросов (20 минут)

### Задача 3.1: Эффективная обработка списка

**Исходные данные:**
```python
products = [
    "iPhone 15 Pro",
    "Samsung Galaxy S24",
    "Google Pixel 9",
    "OnePlus 12"
]
```

**Что нужно сделать:**

**Вариант A (неэффективный)** — отправить по одному запросу на каждый товар в цикле:

```python
for product in products:
    response = client.chat.completions.create(...)
    # ... обработка
```

**Вариант B (батчинг)** — передать весь список в одном запросе через системное сообщение:

```python
messages = [
    {
        "role": "system",
        "content": "Тебе передают список смартфонов. Для каждого укажи: бренд, ОС и примерную цену в USD. Отвечай по каждому отдельной строкой."
    },
    {
        "role": "user",
        "content": ", ".join(products)
    }
]
```

Реализуйте оба варианта, подсчитайте суммарное количество токенов в каждом и сравните:

**Ожидаемый результат:**
```
=== ВАРИАНТ A: по одному запросу ===
[Результаты для каждого товара]
Суммарно токенов: XXX

=== ВАРИАНТ B: батчинг ===
[Результаты всех товаров в одном ответе]
Суммарно токенов: XXX

=== СРАВНЕНИЕ ===
Батчинг сэкономил X токенов (X%)
```

---

### Задача 3.2: Батчинг с JSON-выводом

**Что нужно сделать:**

Повторите батчинг из задачи 3.1, но запросите результат в JSON-формате — список объектов с полями `name`, `brand`, `os`, `price_usd`. Распарсите и выведите данные в виде таблицы:

```
Название              | Бренд    | ОС        | Цена ($)
----------------------------------------------------------
iPhone 15 Pro         | Apple    | iOS       | 1199
...
```

**Шаблон кода:**
```python
response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL"),
    messages=[
        {
            "role": "system",
            "content": # Ваш системный промпт с инструкцией вернуть JSON
        },
        {
            "role": "user",
            "content": ", ".join(products)
        }
    ],
    response_format={"type": "json_object"}
)

# Ваш код: распарсить и вывести таблицу
```

---

## Часть 4: Retry-логика с Tenacity (20 минут)

### Задача 4.1: Декоратор повторных попыток

**Что нужно сделать:**

1. Оберните вызов API декоратором `@retry` из библиотеки `tenacity` со следующими параметрами:
   - Экспоненциальный откат: от 1 до 30 секунд
   - Максимум 4 попытки
   - Повторять только при `openai.RateLimitError` и `openai.APIConnectionError`

2. Добавьте вывод сообщения перед каждой повторной попыткой: `"[RETRY] Попытка #N..."`

3. Вызовите функцию и убедитесь, что при успешном запросе вывод корректный.

**Шаблон кода:**
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep
)
import openai

def log_retry(retry_state):
    print(f"[RETRY] Попытка #{retry_state.attempt_number}...")

@retry(
    retry=retry_if_exception_type((# Ваш код: типы ошибок для повтора)),
    stop=stop_after_attempt(# Ваш код),
    wait=wait_exponential(min=# Ваш код, max=# Ваш код),
    before_sleep=log_retry
)
def resilient_request(prompt):
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Проверка
result = resilient_request("Назови 3 языка программирования одной строкой.")
print(result)
```

---

### Задача 4.2: Совмещение retry и обработки ошибок

**Что нужно сделать:**

Объедините retry-логику и обработку ошибок из части 2 в одну функцию `production_request(prompt)`:

- При `RateLimitError` или `APIConnectionError` — повторять (до 4 раз, с задержкой 1–30 сек)
- При `AuthenticationError` — не повторять, вывести сообщение об ошибке и вернуть `None`
- При `BadRequestError` — не повторять, вывести детали и вернуть `None`
- При любой другой ошибке — не повторять, вывести и вернуть `None`

```python
def production_request(prompt):
    # Ваш код: объедините @retry и try/except
    pass

# Тесты
print(production_request("Привет!"))                         # Успех
print(production_request(""))                                 # Возможно BadRequestError
```

---

## Часть 5: Подсчёт токенов (15 минут)

### Задача 5.1: Анализ промптов

**Что нужно сделать:**

Используя библиотеку `tiktoken`, подсчитайте количество токенов в следующих промптах и выведите результаты в виде таблицы:

```python
prompts = {
    "Короткий": "Привет!",
    "Средний": "Напиши краткое резюме для специалиста по данным с опытом 5 лет в Python и машинном обучении.",
    "Длинный": "Ты опытный технический интервьюер. Задай 10 вопросов кандидату на позицию Senior Data Scientist, охватив темы: статистика, машинное обучение, программирование на Python, работа с большими данными и лидерские навыки. После каждого вопроса укажи, какую компетенцию он проверяет."
}
```

**Шаблон кода:**
```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

print(f"{'Промпт':<12} | {'Символов':>10} | {'Токенов':>10} | {'Символов/токен':>15}")
print("-" * 55)

for name, prompt in prompts.items():
    num_chars = len(prompt)
    num_tokens = # Ваш код: подсчитать токены
    ratio = num_chars / num_tokens
    print(f"{name:<12} | {num_chars:>10} | {num_tokens:>10} | {ratio:>14.2f}")
```

**Ожидаемый результат:**
```
Промпт       |   Символов |    Токенов | Символов/токен
-------------------------------------------------------
Короткий     |          7 |          3 |           2.33
Средний      |         XX |         XX |           X.XX
Длинный      |        XXX |        XXX |           X.XX
```

---

### Задача 5.2: Предварительная проверка перед отправкой

**Что нужно сделать:**

Напишите функцию `check_and_send(prompt, max_tokens=500)`, которая:

1. Подсчитывает количество токенов в промпте
2. Если токенов больше `max_tokens` — выводит предупреждение и **не отправляет** запрос:
   ```
   [WARNING] Промпт содержит XXX токенов, превышает лимит XXX. Запрос не отправлен.
   ```
3. Если токенов меньше или равно `max_tokens` — отправляет запрос и выводит:
   ```
   [OK] Промпт содержит XXX токенов. Отправляю запрос...
   [ОТВЕТ] ...
   ```

Проверьте функцию на коротком промпте (должен пройти) и длинном (должен быть заблокирован):

```python
short_prompt = "Назови столицу России."
long_prompt = "Напиши " + "очень длинный промпт " * 50

check_and_send(short_prompt, max_tokens=500)
print()
check_and_send(long_prompt, max_tokens=500)
```

---

## Бонусное задание (необязательно, +20 минут)

### Задача 6: Мини-пайплайн обработки данных

**Сценарий:** Вы разрабатываете систему автоматической обработки отзывов о книгах.

**Исходные данные:**
```python
reviews = [
    "This book changed my life! The author explains machine learning concepts in a way that's both accessible and deep. Highly recommend to anyone in data science.",
    "Disappointing. The examples are outdated and the explanations are too shallow. Expected much more from this title.",
    "Good introduction, but lacks depth on neural networks. Decent for beginners, frustrating for intermediate readers."
]
```

**Что нужно сделать:**

Реализуйте пайплайн, который для каждого отзыва:

1. **Переводит** на русский язык (отдельный запрос)
2. **Классифицирует** настроение в JSON-формате: `{"sentiment": "positive|neutral|negative", "score": 1-5}`
3. **Проверяет токены** перед каждым запросом (лимит: 300 токенов на промпт)
4. **Обрабатывает ошибки** через try/except
5. **Считает итоговую статистику**

**Ожидаемый результат:**
```
=== ОБРАБОТКА ОТЗЫВА 1 ===
[OK] Проверка токенов пройдена (XX токенов)
Перевод: [текст на русском]
Настроение: positive (5/5)

=== ОБРАБОТКА ОТЗЫВА 2 ===
...

=== ИТОГ ===
Обработано: 3/3
Positive: X | Neutral: X | Negative: X
Средняя оценка: X.X/5
Всего токенов использовано: XXX
```

---

## Критерии оценки

| Часть | Баллы | Критерий |
|-------|-------|----------|
| Часть 1 | 20 | JSON-формат запрашивается корректно, ответ парсится и обрабатывается |
| Часть 2 | 25 | Все типы ошибок обрабатываются раздельно, логирование работает |
| Часть 3 | 20 | Оба варианта реализованы, сравнение токенов выведено |
| Часть 4 | 20 | Retry настроен корректно, объединение с обработкой ошибок работает |
| Часть 5 | 15 | Подсчёт токенов точный, предварительная проверка работает |
| Бонус | 20 | Полный пайплайн работает со всеми элементами |
| **Всего** | **100** | |

## Рекомендации по выполнению

1. **Начните с части 1** — структурированный JSON — это основа для всех последующих задач
2. **Тестируйте сценарии ошибок постепенно**: начните с AuthenticationError (легко воспроизвести), затем BadRequestError
3. **При работе с tenacity**: запустите корректный запрос сначала, убедитесь что без ошибок — только потом проверяйте retry
4. **Сравнение токенов в части 3**: обратите внимание, что батчинг экономит токены за счёт общего системного промпта
5. **Для бонусного задания**: разбейте на маленькие функции — по одной на каждый шаг пайплайна

## Что вы освоите

После выполнения этого задания вы сможете:
- ✅ Запрашивать и парсить структурированные JSON-ответы от API
- ✅ Грамотно обрабатывать разные типы ошибок OpenAI API
- ✅ Оптимизировать число запросов через батчинг
- ✅ Реализовывать retry-логику с экспоненциальным откатом
- ✅ Контролировать количество токенов до отправки запроса
- ✅ Строить production-ready пайплайны обработки текста

---

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]]*
