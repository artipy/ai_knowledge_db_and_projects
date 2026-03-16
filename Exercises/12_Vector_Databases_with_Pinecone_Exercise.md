# Практическое задание №12: Векторные базы данных с Pinecone

## Цель задания

Освоить работу с облачной векторной базой данных Pinecone: создание serverless-индексов, подключение и инспекция индекса, загрузка векторов с метаданными через `upsert`, поиск ближайших соседей с фильтрацией по метаданным и управление жизненным циклом индекса.

## Связанные материалы

- [[OpenAI_API/Vector_Databases_with_Pinecone|Векторные базы данных с Pinecone]]
- [[OpenAI_API/Vector_Databases_with_ChromaDB|Векторные базы данных с ChromaDB]]
- [[OpenAI_API/Working_with_Embeddings|Работа с Embeddings]]
- [[OpenAI_API/Embeddings_Applications|Применение Embeddings: поиск, рекомендации и классификация]]

## Следующие шаги

Это задание является продолжением [[Exercises/11_Vector_Databases_with_ChromaDB_Exercise|Практического задания №11]]. После выполнения вы освоите работу с production-ready managed векторной базой данных и поймёте разницу между Pinecone и ChromaDB в реальных сценариях.

## Предварительные требования

- Выполненные задания №9–11 (понимание эмбеддингов, cosine similarity, ChromaDB)
- Учётная запись Pinecone (бесплатный план Starter на [pinecone.io](https://pinecone.io))
- Настроенный `.env` файл с API ключами
- Установленные библиотеки: `pinecone`, `openai`, `python-dotenv`, `tiktoken`

```python
# Установка зависимостей
# pip install pinecone openai python-dotenv tiktoken
```

**Получение API ключа Pinecone:**
1. Зарегистрируйтесь на pinecone.io → план Starter
2. Перейдите на страницу «API Keys»
3. Скопируйте ключ в `.env` как `PINE_API=your_key_here`

---

## Исходные данные

Во всех частях задания используется тот же набор новостных статей, что и в задании №11:

```python
articles = [
    {"id": "art-01", "headline": "SpaceX Launches New Starship Rocket",
     "topic": "Science", "year": 2024,
     "keywords": ["space", "rocket", "nasa", "exploration"]},
    {"id": "art-02", "headline": "Bitcoin Reaches All-Time High as Investors Rush In",
     "topic": "Business", "year": 2024,
     "keywords": ["crypto", "bitcoin", "finance", "investment"]},
    {"id": "art-03", "headline": "Champions League Final: Real Madrid vs Manchester City",
     "topic": "Sport", "year": 2023,
     "keywords": ["football", "soccer", "champions league", "madrid"]},
    {"id": "art-04", "headline": "New AI Model Outperforms Humans in Medical Diagnosis",
     "topic": "Tech", "year": 2024,
     "keywords": ["ai", "healthcare", "machine learning", "diagnosis"]},
    {"id": "art-05", "headline": "Global Leaders Meet to Discuss Climate Change",
     "topic": "Science", "year": 2023,
     "keywords": ["climate", "environment", "policy", "emissions"]},
    {"id": "art-06", "headline": "Apple Announces Revolutionary New iPhone",
     "topic": "Tech", "year": 2024,
     "keywords": ["apple", "iphone", "smartphone", "technology"]},
    {"id": "art-07", "headline": "Stock Markets Plunge Amid Recession Fears",
     "topic": "Business", "year": 2023,
     "keywords": ["stocks", "economy", "recession", "wall street"]},
    {"id": "art-08", "headline": "Olympics 2024: USA Wins Gold in Swimming",
     "topic": "Sport", "year": 2024,
     "keywords": ["olympics", "swimming", "usa", "gold medal"]},
    {"id": "art-09", "headline": "Scientists Discover New Species in Amazon Rainforest",
     "topic": "Science", "year": 2023,
     "keywords": ["biology", "amazon", "species", "nature"]},
    {"id": "art-10", "headline": "Tesla Unveils Autonomous Robot for Home Use",
     "topic": "Tech", "year": 2024,
     "keywords": ["tesla", "robot", "automation", "ai"]},
]
```

---

## Часть 1: Создание индекса (20 минут)

### Задача 1.1: Инициализация клиента Pinecone

**Что нужно сделать:**

1. Импортируйте `Pinecone` и `ServerlessSpec` из пакета `pinecone`
2. Загрузите переменные окружения и создайте клиент `pc`, передав API ключ из `.env`
3. Создайте serverless-индекс с именем `news-index`, размерностью `1536` (модель `text-embedding-3-small`), облачным провайдером `aws` и регионом `us-east-1`
4. Убедитесь, что индекс создан, вызвав `pc.list_indexes()`

**Ожидаемый результат:**
```
[{'name': 'news-index', 'metric': 'cosine', 'dimension': 1536, ...}]
```

**Шаблон кода:**
```python
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()

# Создайте клиент Pinecone
pc = Pinecone(api_key=...)

# Создайте serverless-индекс
pc.create_index(
    name=...,
    dimension=...,
    spec=ServerlessSpec(
        cloud=...,
        region=...
    )
)

print(pc.list_indexes())
```

> **Важно:** Если индекс с таким именем уже существует, вы получите ошибку. Убедитесь, что имя уникально, или удалите существующий индекс перед повторным запуском.

### Задача 1.2: Оценка стоимости эмбеддингов

**Что нужно сделать:**

1. Реализуйте функцию `create_article_text(article)`, которая объединяет поля в строку:
```
Headline: <заголовок>
Topic: <тема>
Keywords: <слово1>, <слово2>, ...
```
2. С помощью `tiktoken` подсчитайте общее количество токенов для всех статей
3. Рассчитайте стоимость при цене `$0.00002` за 1000 токенов (модель `text-embedding-3-small`)

**Ожидаемый результат:**
```
Total tokens: ~100-200
Cost: $0.0000XX
```

**Шаблон кода:**
```python
import tiktoken

def create_article_text(article):
    # Ваш код здесь
    pass

article_texts = [create_article_text(a) for a in articles]

encoder = tiktoken.encoding_for_model('text-embedding-3-small')
total_tokens = ...
cost_per_1k = 0.00002
cost = ...

print(f'Total tokens: {total_tokens}')
print(f'Cost: ${cost:.6f}')
```

---

## Часть 2: Управление индексом (15 минут)

### Задача 2.1: Подключение к индексу и статистика

**Что нужно сделать:**

1. Подключитесь к созданному индексу с помощью `pc.Index('news-index')` и сохраните результат в переменную `index`
2. Вызовите `index.describe_index_stats()` и выведите результат
3. Обратите внимание на поля `dimension`, `total_vector_count`, `index_fullness` и `namespaces`

**Ожидаемый результат:**
```python
{
    'dimension': 1536,
    'index_fullness': 0.0,
    'total_vector_count': 0,
    'namespaces': {},
    ...
}
```

**Шаблон кода:**
```python
# Подключитесь к индексу
index = pc.Index(...)

# Получите статистику
stats = index.describe_index_stats()
print(stats)

print(f"\nРазмерность индекса: {stats['dimension']}")
print(f"Количество векторов: {stats['total_vector_count']}")
print(f"Заполненность: {stats['index_fullness']}")
```

### Задача 2.2: Обработка ошибки несуществующего индекса

**Что нужно сделать:**

Попробуйте подключиться к индексу с несуществующим именем и перехватите исключение. Выведите сообщение об ошибке.

**Шаблон кода:**
```python
try:
    error_index = pc.Index('non-existent-index')
    error_index.describe_index_stats()
except Exception as e:
    print(f'Ошибка: {type(e).__name__}: {e}')
```

> **Что происходит:** Pinecone вернёт ошибку 404, если индекс не найден. Это важно учитывать при разработке production-приложений.

---

## Часть 3: Загрузка векторов (25 минут)

### Задача 3.1: Создание эмбеддингов через OpenAI

**Что нужно сделать:**

1. Используя OpenAI API, создайте эмбеддинги для всех статей (используйте `article_texts` из задачи 1.2)
2. Сформируйте список словарей `vectors` в формате Pinecone: каждый словарь должен содержать поля `id` и `values`
3. Проверьте размерность каждого вектора с помощью list comprehension и функции `all()`

**Ожидаемый результат:**
```
Размерность всех векторов корректна: True
Пример вектора: {'id': 'art-01', 'values': [0.0123, ..., 0.0456]}
```

**Шаблон кода:**
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Создайте эмбеддинги для всех текстов
response = client.embeddings.create(
    input=...,
    model='text-embedding-3-small'
)

# Сформируйте список векторов для Pinecone
vectors = [
    {
        'id': articles[i]['id'],
        'values': ...  # вектор из response
    }
    for i in range(len(articles))
]

# Проверьте размерность
vector_dims = [len(v['values']) == 1536 for v in vectors]
print(f'Размерность всех векторов корректна: {all(vector_dims)}')
print(f"Пример вектора: {{'id': '{vectors[0][\"id\"]}', 'values': [{vectors[0]['values'][0]:.4f}, ..., {vectors[0]['values'][-1]:.4f}]}}")
```

> **Подсказка:** Эмбеддинги находятся в `response.data[i].embedding`.

### Задача 3.2: Загрузка векторов через upsert

**Что нужно сделать:**

1. Загрузите все векторы в индекс одним вызовом `index.upsert()`
2. Вызовите `index.describe_index_stats()` и убедитесь, что векторы появились в индексе

**Ожидаемый результат:**
```
Векторов в индексе: 10
```

**Шаблон кода:**
```python
# Загрузите векторы
index.upsert(vectors=...)

# Проверьте результат
stats = index.describe_index_stats()
print(f"Векторов в индексе: {stats['total_vector_count']}")
```

> **Важно:** Обновление статистики может занять несколько секунд. Если `total_vector_count` равен 0 — подождите и повторите вызов.

---

## Часть 4: Метаданные и upsert-семантика (20 минут)

### Задача 4.1: Повторный upsert (идемпотентность)

**Что нужно сделать:**

1. Загрузите те же 10 векторов повторно через `upsert`
2. Вызовите `describe_index_stats()` и убедитесь, что количество векторов **не изменилось** (осталось 10)
3. Запишите вывод в комментарий — объясните своими словами, почему это происходит

**Шаблон кода:**
```python
index.upsert(vectors=vectors)  # повторная загрузка тех же данных

stats = index.describe_index_stats()
print(f"Векторов в индексе: {stats['total_vector_count']}")
# Ожидаемый результат: 10 (не 20!)
# Почему? # Ваш комментарий здесь
```

### Задача 4.2: Добавление метаданных к векторам

**Что нужно сделать:**

1. Сформируйте новый список векторов `vectors_with_meta`, добавив к каждому словарю поле `metadata` с полями `topic` и `year`
2. Загрузите обновлённые векторы через `upsert` — существующие записи обновятся, новых не добавится
3. Добавьте новую статью с ID `art-11` через `upsert`:

```python
new_article = {
    "id": "art-11",
    "headline": "Ethereum Surges 30% Following Network Upgrade",
    "topic": "Business",
    "year": 2024,
    "keywords": ["ethereum", "crypto", "blockchain", "investment"]
}
```

4. Проверьте, что количество векторов стало 11

**Ожидаемый результат:**
```
Векторов после добавления новой статьи: 11
```

**Шаблон кода:**
```python
# Обновите векторы — добавьте метаданные
vectors_with_meta = [
    {
        'id': articles[i]['id'],
        'values': vectors[i]['values'],
        'metadata': {
            'topic': ...,
            'year': ...
        }
    }
    for i in range(len(articles))
]

index.upsert(vectors=vectors_with_meta)

# Создайте эмбеддинг для новой статьи
new_article = {
    "id": "art-11",
    "headline": "Ethereum Surges 30% Following Network Upgrade",
    "topic": "Business",
    "year": 2024,
    "keywords": ["ethereum", "crypto", "blockchain", "investment"]
}

new_response = client.embeddings.create(
    input=[create_article_text(new_article)],
    model='text-embedding-3-small'
)

index.upsert(vectors=[{
    'id': new_article['id'],
    'values': ...,
    'metadata': {'topic': new_article['topic'], 'year': new_article['year']}
}])

stats = index.describe_index_stats()
print(f"Векторов после добавления новой статьи: {stats['total_vector_count']}")
```

---

## Часть 5: Поиск и фильтрация (25 минут)

### Задача 5.1: Семантический поиск

**Что нужно сделать:**

1. Создайте эмбеддинг для каждого из трёх поисковых запросов ниже
2. Для каждого запроса вызовите `index.query()` с `top_k=3` и `include_metadata=True`
3. Выведите топ-3 результата с заголовками статей и оценками сходства (`score`)

**Поисковые запросы:**
```python
queries = [
    "artificial intelligence and robotics",
    "financial crisis and investment",
    "olympic games and athletic achievements",
]
```

**Ожидаемый результат:**
```
Запрос: "artificial intelligence and robotics"
  1. art-04 | score=0.XXXX | metadata: {'topic': 'Tech', 'year': 2024}
  2. art-10 | score=0.XXXX | ...
  3. art-06 | score=0.XXXX | ...
```

**Шаблон кода:**
```python
for query_text in queries:
    query_response = client.embeddings.create(
        input=[query_text],
        model='text-embedding-3-small'
    )
    query_vector = ...

    result = index.query(
        vector=...,
        top_k=...,
        include_metadata=...
    )

    print(f'Запрос: "{query_text}"')
    for match in result['matches']:
        print(f"  {match['id']} | score={match['score']:.4f} | metadata: {match['metadata']}")
    print()
```

> **Подсказка:** Структура ответа Pinecone: `result['matches']` — список словарей с полями `id`, `score`, `metadata`.

### Задача 5.2: Поиск с фильтрацией по метаданным

**Что нужно сделать:**

Выполните три поисковых запроса с фильтром `filter`:

1. Запрос `"technology and innovation"` — только `topic = Tech`
2. Запрос `"science discoveries"` — только `year = 2023`
3. Запрос `"sports championships"` — исключить `topic = Business` (оператор `$ne`)

**Ожидаемый результат:**
```
=== Только Tech ===
  art-04 | score=0.XXXX
  art-06 | score=0.XXXX
  art-10 | score=0.XXXX

=== Только 2023 год ===
  ...

=== Исключая Business ===
  ...
```

**Шаблон кода:**
```python
# Запрос 1: фильтр по topic
q1_vector = client.embeddings.create(input=['technology and innovation'], model='text-embedding-3-small').data[0].embedding

result = index.query(
    vector=q1_vector,
    top_k=3,
    include_metadata=True,
    filter={'topic': {'$eq': 'Tech'}}
)
print('=== Только Tech ===')
for match in result['matches']:
    print(f"  {match['id']} | score={match['score']:.4f}")

# Запрос 2: фильтр по году
q2_vector = client.embeddings.create(input=['science discoveries'], model='text-embedding-3-small').data[0].embedding

result = index.query(
    vector=q2_vector,
    top_k=3,
    include_metadata=True,
    filter={'year': {'$eq': ...}}
)
print('\n=== Только 2023 год ===')
...

# Запрос 3: оператор $ne
q3_vector = client.embeddings.create(input=['sports championships'], model='text-embedding-3-small').data[0].embedding

result = index.query(
    vector=q3_vector,
    top_k=3,
    include_metadata=True,
    filter={'topic': {'$ne': ...}}
)
print('\n=== Исключая Business ===')
...
```

### Задача 5.3: Рекомендательная система

**Сценарий:** Пользователь читает статью о криптовалюте. Система должна предложить похожие материалы только из темы Business, исключив саму прочитанную статью.

**Что нужно сделать:**

1. Используйте вектор статьи `art-02` как запрос (уже находится в индексе — создайте эмбеддинг из текста статьи)
2. Выполните поиск с `top_k=4` и фильтром `topic = Business`
3. Из результатов исключите `art-02` в постобработке
4. Выведите финальные рекомендации

**Ожидаемый результат:**
```
Эталонная статья: "Bitcoin Reaches All-Time High as Investors Rush In"

Рекомендации (только Business):
  1. art-07 | Stock Markets Plunge Amid Recession Fears | score=0.XXXX
  2. art-11 | Ethereum Surges 30% Following Network Upgrade | score=0.XXXX
```

**Шаблон кода:**
```python
reference_article = articles[1]  # art-02
reference_text = create_article_text(reference_article)

ref_vector = client.embeddings.create(
    input=[reference_text],
    model='text-embedding-3-small'
).data[0].embedding

result = index.query(
    vector=ref_vector,
    top_k=4,
    include_metadata=True,
    filter={'topic': 'Business'}
)

print(f'Эталонная статья: "{reference_article["headline"]}"\n')
print('Рекомендации (только Business):')
rank = 1
for match in result['matches']:
    if match['id'] == reference_article['id']:
        continue  # исключаем эталонную статью
    # найдите заголовок по ID из списка articles
    headline = next((a['headline'] for a in articles if a['id'] == match['id']), match['id'])
    print(f"  {rank}. {match['id']} | {headline} | score={match['score']:.4f}")
    rank += 1
```

---

## Бонусное задание (необязательно, +20 минут)

### Задача 6: Пространства имён (Namespaces)

**Что нужно сделать:**

1. Загрузите статьи категории `Tech` в пространство имён `tech-namespace`
2. Загрузите статьи категории `Business` в пространство имён `business-namespace`
3. Вызовите `describe_index_stats()` и убедитесь, что оба namespace отображаются в статистике
4. Выполните поиск по запросу `"artificial intelligence"` **только** в `tech-namespace`

**Шаблон кода:**
```python
# Отфильтруйте статьи по теме
tech_vectors = [v for v, a in zip(vectors_with_meta, articles) if a['topic'] == 'Tech']
business_vectors = [v for v, a in zip(vectors_with_meta, articles) if a['topic'] == 'Business']

# Загрузите в разные пространства имён
index.upsert(vectors=tech_vectors, namespace='tech-namespace')
index.upsert(vectors=business_vectors, namespace='business-namespace')

# Проверьте статистику
stats = index.describe_index_stats()
print('Namespaces:', stats['namespaces'])

# Поиск только в tech-namespace
query_vector = client.embeddings.create(
    input=['artificial intelligence'],
    model='text-embedding-3-small'
).data[0].embedding

result = index.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True,
    namespace=...
)
print('\nРезультаты в tech-namespace:')
for match in result['matches']:
    print(f"  {match['id']} | score={match['score']:.4f}")
```

---

## Очистка (обязательно выполнить в конце)

```python
# Удаление индекса освобождает ресурсы на бесплатном плане
pc.delete_index('news-index')
print('Индекс удалён.')
print('Оставшиеся индексы:', pc.list_indexes())
```

> **Важно:** На бесплатном плане Pinecone ограниченное количество индексов. Удаляйте неиспользуемые индексы после завершения работы.

---

## Критерии оценки

| Часть | Баллы | Критерий |
|-------|-------|----------|
| Часть 1 | 15 | Создание клиента, индекса, оценка стоимости токенов |
| Часть 2 | 10 | Подключение к индексу, `describe_index_stats`, обработка ошибки 404 |
| Часть 3 | 20 | Создание эмбеддингов через OpenAI, проверка размерности, `upsert` |
| Часть 4 | 20 | Идемпотентность `upsert`, добавление метаданных, новая запись |
| Часть 5 | 35 | Семантический поиск, фильтрация `$eq/$ne`, рекомендательная система |
| Бонус  | 20 | Пространства имён, поиск в конкретном namespace |
| **Всего** | **100** | |

---

## Рекомендации по выполнению

1. **Размерность индекса**: при создании индекса `dimension` должна точно совпадать с размерностью выбранной модели эмбеддингов — `text-embedding-3-small` возвращает 1536 измерений
2. **`upsert` идемпотентен**: повторный вызов с теми же ID обновит данные, но не создаст дубликаты — это ключевое отличие от простого `insert`
3. **Задержка обновления статистики**: `describe_index_stats()` обновляется с небольшой задержкой — если `total_vector_count` не изменился сразу после `upsert`, подождите несколько секунд
4. **Структура ответа `query`**: результаты находятся в `result['matches']`, каждый элемент содержит `id`, `score` (0–1, чем выше — тем лучше) и `metadata`
5. **Фильтрация**: операторы Pinecone аналогичны ChromaDB — `$eq`, `$ne`, `$gt`, `$lt`, `$and`, `$or`
6. **Удаление индекса**: всегда удаляйте тестовые индексы по завершении работы — на бесплатном плане ограниченное количество индексов

## Что вы освоите

После выполнения этого задания вы сможете:
- Создавать serverless-индексы в Pinecone и управлять их жизненным циклом
- Генерировать эмбеддинги через OpenAI API и загружать их в Pinecone
- Использовать `upsert` для атомарного добавления и обновления записей
- Выполнять семантический поиск с фильтрацией по метаданным
- Строить рекомендательные системы на базе managed векторной БД
- Понимать разницу между Pinecone и ChromaDB при выборе инструмента

---

**Удачи в выполнении задания!**

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Vector_Databases_with_Pinecone|Векторные базы данных с Pinecone]]*
