# Структурирование end-to-end приложений на OpenAI API

Эта заметка охватывает ключевые аспекты создания production-ready приложений на базе OpenAI API: структурирование вызовов, обработку ошибок, управление rate limits и подсчёт токенов.

## Связанные заметки

- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - базовые концепции подключения и работы с API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - практические примеры вызовов и параметров
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]] - подробное руководство по retry-паттернам
- [[Python_for_AI/Python_Decorators|Декораторы в Python]] - основы декораторов, используемых в tenacity

## Структурирование вызова API

Базовый вызов API — это лишь отправная точка. Для production-окружения вызов должен:

- обрабатывать ошибки в удобном для пользователя виде
- включать функции модерации и безопасности
- поддерживать тестирование и валидацию
- легко интегрироваться с внешними системами

### Запрос в формате JSON

Для лучшей интеграции с внешними приложениями ответ модели следует запрашивать в структурированном формате. Параметр `response_format` позволяет задать тип `json_object`:

```python
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

def clean_response(text):
    """Убирает теги <think>...</think> из ответа модели."""
    pattern = r"<think>.*?</think>"
    return re.sub(pattern, "", text, flags=re.DOTALL).strip()

client = OpenAI(
    api_key=os.getenv('GROQ_TOKEN'),
    base_url=os.getenv('BASE_URL_GROQ')
)

response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=[
        {
            'role': 'user',
            'content': 'Сгенерируй 5 наименований деревьев с их научным названием в формате json'
        }
    ],
    response_format={'type': 'json_object'}
)

content = response.choices[0].message.content
print(clean_response(content))
```

**Результат:**
```json
[
  {"name": "Дуб обыкновенный", "scientific_name": "Quercus robur"},
  {"name": "Ель обыкновенная", "scientific_name": "Pinus sylvestris"},
  {"name": "Береза повислая",  "scientific_name": "Betula pendula"},
  {"name": "Клён полевой",     "scientific_name": "Acer campestre"},
  {"name": "Липа мелколистная","scientific_name": "Tilia cordata"}
]
```

> **Важно**: при использовании `response_format={'type': 'json_object'}` необходимо также явно указать формат JSON в тексте промпта — иначе модель может вернуть ошибку.

## Обработка ошибок

Ошибки OpenAI API делятся на несколько категорий:

| Тип ошибки | Причина | Решение |
|---|---|---|
| `InternalServerError`, `APIConnectionError`, `APITimeoutError` | Проблемы с соединением или сервером | Проверить сеть, подождать и повторить |
| `RateLimitError`, `ConflictError` | Превышены лимиты запросов или токенов | Уменьшить объём или распределить запросы во времени |
| `AuthenticationError` | Недействительный или просроченный API-ключ | Проверить и обновить ключ |
| `BadRequestError` | Неверные параметры запроса (например, невалидная роль) | Проверить документацию и входные параметры |

### Обработка через try/except

Инкапсуляция вызова в `try/except` позволяет программе продолжить работу при ошибках:

```python
import openai

try:
    response = client.chat.completions.create(
        model=os.getenv('GROQ_MODEL'),
        messages=[
            {
                'role': 'user',
                'content': 'Сгенерируй 5 наименований деревьев с их научным названием в формате json'
            }
        ],
        response_format={'type': 'json_object'}
    )
    content = response.choices[0].message.content
    print(clean_response(content))

except openai.AuthenticationError as e:
    print(f'OpenAI API failed to authenticate: {e}')
except openai.RateLimitError as e:
    print(f'OpenAI API request exceeded rate limit: {e}')
except Exception as e:
    print(f'Unable to generate a response. Exception: {e}')
```

## Батчинг и управление Rate Limits

Ограничения скорости API (rate limits) регулируют поток данных между пользователями и сервисом. Превышение лимита возникает из-за:

- **Слишком высокой частоты запросов** — слишком много вызовов за единицу времени
- **Слишком большого количества токенов** — в запросе передаётся избыточный текст

### Retry с экспоненциальным откатом (tenacity)

Библиотека `tenacity` позволяет автоматически повторять запрос при достижении лимита. Декоратор `@retry` добавляет retry-логику без изменения внутренней логики функции:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_response(message):
    response = client.chat.completions.create(
        model=os.getenv('GROQ_MODEL'),
        messages=[
            {
                'role': 'user',
                'content': message
            }
        ]
    )
    answer = response.choices[0].message.content
    return clean_response(answer)
```

**Параметры `wait_random_exponential`:**
- `min` — минимальная задержка перед повторной попыткой (в секундах)
- `max` — максимальная задержка (в секундах)

**Параметр `stop_after_attempt`** — максимальное количество попыток.

Подробнее о стратегиях retry см. [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]].

### Батчинг запросов

Если ограничение связано с частотой запросов, эффективнее отправить один запрос с несколькими вопросами, чем несколько запросов в цикле:

```python
countries = ['United States', 'Ireland', 'India']

messages = [
    {
        'role': 'system',
        'content': 'Тебе передают список стран и спрашивают столицу и название страны. Предоставь ответ по каждому вопросу как разделенный контент.'
    }
]

messages.append({'role': 'user', 'content': ','.join(countries)})

response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=messages
)

print(response.choices[0].message.content)
```

Этот подход значительно эффективнее циклического прохода, где каждая страна отправляется отдельным запросом.

## Подсчёт токенов (tiktoken)

Если ограничение связано с количеством токенов, нужно измерить объём промпта заранее. Библиотека `tiktoken` позволяет подсчитать количество токенов для любой строки:

```python
import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4o-mini')

prompt = "Какой нибудь промпт кол-во токенов которого мы бы хотели посчитать!"

num_tokens = len(encoding.encode(prompt))

print(f'Кол-во токенов в запросе: {num_tokens}')
# Кол-во токенов в запросе: 23
```

Это позволяет:
- заранее убедиться, что промпт не превышает лимиты модели
- оценить стоимость запроса до его отправки
- динамически усекать текст при необходимости

> Каждая модель имеет собственные ограничения на количество входных токенов. Актуальные лимиты указаны в документации провайдера.

## Рекомендации

1. **Всегда используйте try/except** для вызовов API в production-коде
2. **Разделяйте типы ошибок**: не повторяйте запрос при `AuthenticationError` — это не временная проблема
3. **Используйте экспоненциальный откат** вместо фиксированной паузы — это снижает нагрузку на сервер
4. **Батчируйте запросы**, когда нужно обработать список однотипных данных
5. **Считайте токены заранее** с помощью `tiktoken`, чтобы контролировать стоимость и избегать ошибок
6. **Указывайте JSON-формат дважды**: в параметре `response_format` и в тексте промпта

## Связанные материалы

- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - основы работы с API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - практические примеры
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]] - системные сообщения и контекст
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]] - подробное руководство по retry
- [[Python_for_AI/Python_Decorators|Декораторы в Python]] - как устроены декораторы изнутри

## Практика

Для закрепления материала выполните практическое задание:
- [[Exercises/07_Structuring_End_to_End_Applications_Exercise|Практическое задание №7]] - JSON-ответы, обработка ошибок, батчинг, retry и подсчёт токенов

---

*Эта заметка создана на основе Jupyter Notebook `raw_notes/13_structuring_end_to_end_applications.ipynb`.*
