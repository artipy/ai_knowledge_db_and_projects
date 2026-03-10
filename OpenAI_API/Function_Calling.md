# Вызов функций (Function Calling)

Вызов функций — это механизм OpenAI API, позволяющий моделям возвращать структурированные ответы с помощью пользовательских функций. В отличие от `response_format: json_object`, где структура ответа зависит от интерпретации модели, функции задают точную схему выходных данных.

## Связанные заметки

- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - базовые концепции подключения и работы с API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - практические примеры вызовов и параметров
- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]] - JSON-ответы, батчинг, обработка ошибок
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]] - системные сообщения и контекст

## Зачем нужен вызов функций

При использовании `response_format: json_object` ключи JSON-ответа формируются моделью самостоятельно и могут быть несогласованными при одних и тех же промптах. Вызов функций решает эту проблему, позволяя задать точную схему ответа.

Пример проблемы с `json_object` — один и тот же промпт может вернуть разные структуры:
```python
response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=[{'role': 'user', 'content': 'Сгенерируй список из 4 деревьев с их научными названиями в формате json'}],
    response_format={'type': 'json_object'}
)
```

Вызов функций устраняет эту нестабильность, обеспечивая:
- **Надёжную структуру** для интеграции с внешними системами
- **Параллельный вызов нескольких функций** в одном запросе
- **Вызов внешних API** на основе естественно-языкового ввода

## Определение функции

Функция передаётся в параметр `tools` как список словарей. Каждый элемент имеет следующую структуру:

```python
function_definition = [
    {
        'type': 'function',       # тип инструмента
        'function': {
            'name': 'extract_job_info',
            'description': 'Get the job information from the body of the input text',
            'parameters': {
                'type': 'object',
                'properties': {
                    'job': {
                        'type': 'string',
                        'description': 'Job title'
                    },
                    'location': {
                        'type': 'string',
                        'description': 'Office location'
                    }
                }
            }
        }
    }
]
```

Ключевые поля:
- `name` — имя функции
- `description` — описание, которое помогает модели выбрать нужную функцию
- `parameters.properties` — словарь параметров с типом и описанием для каждого

## Извлечение структурированных данных

Пример извлечения информации из описания вакансии:

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv('GROQ_TOKEN'),
    base_url=os.getenv('BASE_URL_GROQ')
)

messages = [
    {
        'role': 'user',
        'content': "We are currently seeking a highly skilled Data Scientist at the company's headquarters in San Francisco, CA. Requirements: Minimum 3 years of experience in data science with Python and AWS, Azure or GCP"
    }
]

response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=messages,
    tools=function_definition
)

# Ответ вложен в tool_calls[0].function.arguments
print(response.choices[0].message.tool_calls[0].function.arguments)
# {"job": "Data Scientist", "location": "San Francisco, CA"}
```

> **Важно**: при использовании function calling ответ находится в `response.choices[0].message.tool_calls[0].function.arguments`, а не в `response.choices[0].message.content`.

## Параллельный вызов нескольких функций

Несколько функций можно передать в один вызов API. Модель сама решает, какие из них вызвать на основе запроса. Это называется **параллельным вызовом функций**.

```python
# Добавляем вторую функцию к уже существующей
function_definition.append(
    {
        'type': 'function',
        'function': {
            'name': 'get_timezone',
            'description': 'Return the timezone corresponding to the location in the job advert',
            'parameters': {
                'type': 'object',
                'properties': {
                    'timezone': {
                        'type': 'string',
                        'description': 'Timezone'
                    }
                }
            }
        }
    }
)

response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=messages,
    tools=function_definition
)

# Каждая функция возвращает отдельный элемент в tool_calls
print(response.choices[0].message.tool_calls[0].function.arguments)
# {"job": "Data Scientist", "location": "San Francisco, CA"}
print(response.choices[0].message.tool_calls[1].function.arguments)
# {"timezone": "America/Los_Angeles"}
```

## Управление выбором функции (tool_choice)

По умолчанию модель сама решает, какую функцию вызвать (`tool_choice='auto'`). Это поведение можно изменить:

```python
# Явно указать конкретную функцию
response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=messages,
    tools=function_definition,
    tool_choice={
        'type': 'function',
        'function': {'name': 'extract_job_info'}
    }
)
```

| Значение `tool_choice` | Поведение |
|---|---|
| `'auto'` (по умолчанию) | Модель сама выбирает функцию на основе запроса |
| `{'type': 'function', 'function': {'name': '...'}}` | Принудительно вызывает указанную функцию |

## Предотвращение домыслов модели

Если параметры не найдены в тексте, модель может подставить предполагаемые значения. Чтобы избежать этого, добавьте системное сообщение:

```python
messages = []
messages.append({
    'role': 'system',
    'content': "Don't make assumptions about what values to plug into functions. Don't make up values to fill the response with. Ask for clarification if needed"
})
messages.append({'role': 'user', 'content': 'What is the starting salary for the role?'})
```

В этом случае при отсутствии нужной информации модель вернёт `None` в `message.content` вместо выдуманных данных.

## Вызов внешних API

Вызов функций особенно полезен для интеграции с внешними API: модель извлекает параметры из естественно-языкового ввода, а функция выполняет реальный HTTP-запрос.

Пример: рекомендации произведений искусства из Art Institute of Chicago API:

```python
import requests
import json

def get_artwork(keyword):
    url = 'https://api.artic.edu/api/v1/artwork/search'
    querystring = {'q': keyword}
    response = requests.request('GET', url, params=querystring)
    return response.text

system_prompt = 'You are an AI assistant, a specialist in history of art. You should interpret the user prompt, and based on it extract one keyword for recommending artwork related to their preference.'

user_prompt = "I don't have much time to visit the museum and would like some recommendations. I like the seaside and quiet places"

response = client.chat.completions.create(
    model=os.getenv('GROQ_MODEL'),
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ],
    tools=[
        {
            'type': 'function',
            'function': {
                'name': 'get_artwork',
                'description': 'This function calls the Art Institute of Chicago API to find artwork that matches a keyword',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'artwork keyword': {
                            'type': 'string',
                            'description': 'The keyword to be passed to the get_artwork function'
                        }
                    }
                }
            }
        }
    ]
)
```

### Обработка ответа при вызове внешнего API

```python
if response.choices[0].finish_reason == 'tool_calls':
    function_call = response.choices[0].message.tool_calls[0].function
    if function_call.name == 'get_artwork':
        artwork_keyword = json.loads(function_call.arguments)['artwork keyword']
        artwork = get_artwork(artwork_keyword)
        if artwork:
            titles = [item['title'] for item in json.loads(artwork)['data']]
            print(f'Here are some recommendations: {titles}')
        else:
            print("Apologies, I couldn't make any recommendations based on the request")
    else:
        print("Apologies, I couldn't find any artwork")
else:
    print("I am sorry, but I could not understand your request.")
```

Ключевые шаги обработки:
1. Проверить `finish_reason == 'tool_calls'` — убедиться, что модель вызвала функцию
2. Извлечь имя и аргументы функции из `tool_calls[0].function`
3. Вызвать реальную функцию с извлечёнными аргументами
4. Обработать ответ внешнего API

## Паттерны применения

| Сценарий | Описание |
|---|---|
| Извлечение данных | Структурированное извлечение полей из неструктурированного текста |
| Вызов внешних API | Интеграция с погодой, базами данных, IoT-устройствами |
| Умный дом | Управление устройствами через естественно-языковые команды |
| Чат-бот поддержки | Маршрутизация запросов к разным функциям (каталог, FAQ, ответы) |

## Связанные материалы

- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - основы работы с API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - практические примеры
- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]] - продакшн-паттерны
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]] - системные сообщения

## Практика

Для закрепления материала выполните практическое задание:
- [[Exercises/08_Function_Calling_Exercise|Практическое задание №8]] - определение функций, параллельный вызов, tool_choice, интеграция с внешним API

---

*Эта заметка создана на основе Jupyter Notebook `raw_notes/14_function_calling.ipynb`.*
