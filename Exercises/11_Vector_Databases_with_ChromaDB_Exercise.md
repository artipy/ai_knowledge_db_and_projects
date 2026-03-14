# Практическое задание №11: Векторные базы данных с ChromaDB

## Цель задания

Освоить работу с векторными базами данных на примере ChromaDB: создание коллекций с функцией эмбеддингов, CRUD-операции, семантический поиск с помощью метода `query`, работу с несколькими запросами одновременно, фильтрацию результатов по метаданным и оценку стоимости операций.

## Связанные материалы

- [[OpenAI_API/Vector_Databases_with_ChromaDB|Векторные базы данных с ChromaDB]]
- [[OpenAI_API/Working_with_Embeddings|Работа с Embeddings]]
- [[OpenAI_API/Embeddings_Applications|Применение Embeddings: поиск, рекомендации и классификация]]

## Следующие шаги

Это задание является продолжением [[Exercises/10_Embeddings_Applications_Exercise|Практического задания №10]]. После выполнения вы сможете строить production-ready системы поиска и рекомендаций с персистентным хранилищем векторов.

## Предварительные требования

- Выполненные задания №9 и №10 (понимание эмбеддингов и косинусного расстояния)
- Установленные библиотеки: `chromadb`, `openai`, `python-dotenv`, `tiktoken`
- Настроенный `.env` файл с API ключом

```python
# Установка зависимостей
# pip install chromadb openai python-dotenv tiktoken
```

---

## Исходные данные

Во всех частях задания используется следующий набор новостных статей:

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

## Часть 1: Создание коллекции и загрузка данных (20 минут)

### Задача 1.1: Инициализация ChromaDB

**Что нужно сделать:**

1. Создайте `PersistentClient` с путём к директории `./chroma_db`
2. Создайте коллекцию с именем `news_articles`, передав функцию эмбеддингов OpenAI
3. Проверьте создание коллекции, вызвав `client_db.list_collections()`

**Ожидаемый результат:**
```
[Collection(name=news_articles)]
```

**Шаблон кода:**
```python
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
import os

load_dotenv()

# Создайте PersistentClient
client_db = ...

# Создайте функцию эмбеддингов
embedding_fn = OpenAIEmbeddingFunction(
    api_key=os.getenv('LOCAL_TOKEN'),
    model_name=os.getenv('LOCAL_MODEL'),
    api_base=os.getenv('LOCAL_URL')
)

# Создайте коллекцию
collection = client_db.create_collection(
    name=...,
    embedding_function=...
)

print(client_db.list_collections())
```

### Задача 1.2: Функция формирования текста и оценка стоимости

**Что нужно сделать:**

1. Реализуйте функцию `create_article_text(article)`, которая объединяет поля статьи в строку:
```
Headline: <заголовок>
Topic: <тема>
Keywords: <ключевое слово 1>, <ключевое слово 2>, ...
```

2. С помощью `tiktoken` подсчитайте общее количество токенов для всех статей и рассчитайте стоимость (модель `text-embedding-3-small`, цена `$0.00002` за 1000 токенов)

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

# Подготовьте тексты
article_texts = [create_article_text(a) for a in articles]

# Оцените стоимость
encoder = tiktoken.encoding_for_model('text-embedding-3-small')
total_tokens = ...
cost_per_1k = 0.00002
cost = ...

print(f'Total tokens: {total_tokens}')
print(f'Cost: ${cost:.6f}')
```

### Задача 1.3: Добавление документов с метаданными

**Что нужно сделать:**

1. Из списка `articles` подготовьте три списка: `ids`, `documents` (тексты статей) и `metadatas` (словари с полями `topic` и `year`)
2. Добавьте все документы в коллекцию **одним вызовом** `collection.add()`
3. Проверьте количество документов и просмотрите первые элементы через `peek()`

**Ожидаемый результат:**
```
Документов в коллекции: 10
ids: ['art-01', 'art-02', ...]
```

**Шаблон кода:**
```python
ids = [a['id'] for a in articles]
documents = ...
metadatas = [{'topic': a['topic'], 'year': a['year']} for a in articles]

collection.add(
    ids=...,
    documents=...,
    metadatas=...
)

print(f'Документов в коллекции: {collection.count()}')
print('ids:', collection.peek()['ids'])
```

---

## Часть 2: Запросы к коллекции (20 минут)

### Задача 2.1: Семантический поиск

**Что нужно сделать:**

Получите коллекцию через `client_db.get_collection()` (с функцией эмбеддингов!) и выполните семантический поиск по трём запросам. Для каждого запроса выведите топ-3 результата с заголовками и расстояниями.

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
  1. New AI Model Outperforms Humans in Medical Diagnosis (dist=0.XXXX)
  2. Tesla Unveils Autonomous Robot for Home Use (dist=0.XXXX)
  3. Apple Announces Revolutionary New iPhone (dist=0.XXXX)
```

**Шаблон кода:**
```python
collection = client_db.get_collection(
    name='news_articles',
    embedding_function=...
)

queries = [
    "artificial intelligence and robotics",
    "financial crisis and investment",
    "olympic games and athletic achievements",
]

for query in queries:
    result = collection.query(
        query_texts=...,
        n_results=...
    )
    print(f'Запрос: "{query}"')
    # Обратите внимание: result['documents'] — список списков!
    for i, doc in enumerate(result['documents'][0]):
        dist = result['distances'][0][i]
        # Выведите название статьи и расстояние
        ...
    print()
```

> **Подсказка:** Заголовок нужно извлечь из оригинального словаря `articles` по индексу, либо из самого текста документа.

### Задача 2.2: Несколько запросов одним вызовом

**Что нужно сделать:**

1. Получите тексты двух эталонных статей из коллекции по их ID: `art-02` (криптовалюта) и `art-08` (Олимпиада)
2. Отправьте оба текста как `query_texts` в одном вызове `collection.query()`, запросив по 3 результата
3. Выведите результаты для каждого запроса отдельно

**Ожидаемый результат:**
```
Результаты для запроса 1 (по статье art-02):
  1. Bitcoin Reaches All-Time High... (dist=0.0000)  ← эталонная статья сама себя
  2. Stock Markets Plunge... (dist=0.XXXX)
  3. Federal Reserve... (dist=0.XXXX)

Результаты для запроса 2 (по статье art-08):
  ...
```

**Шаблон кода:**
```python
reference_ids = ['art-02', 'art-08']
reference_texts = collection.get(ids=reference_ids)['documents']

result = collection.query(
    query_texts=...,
    n_results=...
)

for query_idx, query_id in enumerate(reference_ids):
    print(f'Результаты для запроса {query_idx + 1} (по статье {query_id}):')
    for i, (doc, dist) in enumerate(zip(result['documents'][query_idx], result['distances'][query_idx]), 1):
        # Выведите номер, часть текста документа и расстояние
        ...
    print()
```

---

## Часть 3: Обновление коллекции (15 минут)

### Задача 3.1: update и upsert

**Что нужно сделать:**

1. Обновите метаданные статьи `art-03` — добавьте поле `"featured": True` (используйте `update`)
2. Добавьте новую статью через `upsert`. Если запустить `upsert` дважды — данные не дублируются:

```python
new_article = {
    "id": "art-11",
    "headline": "Ethereum Surges 30% Following Network Upgrade",
    "topic": "Business",
    "year": 2024,
    "keywords": ["ethereum", "crypto", "blockchain", "investment"]
}
```

3. Проверьте итоговое количество документов

**Ожидаемый результат:**
```
Документов после upsert: 11
Метаданные art-03: {'topic': 'Sport', 'year': 2023, 'featured': True}
```

**Шаблон кода:**
```python
# Обновите метаданные art-03
collection.update(
    ids=['art-03'],
    metadatas=[{'topic': 'Sport', 'year': 2023, 'featured': True}]
)

# Добавьте новую статью через upsert (запустите дважды — количество не изменится)
new_article = {...}

collection.upsert(
    ids=[new_article['id']],
    documents=[create_article_text(new_article)],
    metadatas=[{'topic': new_article['topic'], 'year': new_article['year']}]
)

print(f'Документов после upsert: {collection.count()}')
print('Метаданные art-03:', collection.get('art-03')['metadatas'][0])
```

### Задача 3.2: Удаление документов

**Что нужно сделать:**

1. Удалите только что добавленную статью `art-11`
2. Убедитесь, что количество документов вернулось к 10

**Шаблон кода:**
```python
collection.delete(ids=[...])
print(f'Документов после удаления: {collection.count()}')
```

---

## Часть 4: Фильтрация по метаданным (25 минут)

### Задача 4.1: Простые фильтры

**Что нужно сделать:**

Выполните три поисковых запроса с фильтрами `where`:

1. Найдите топ-3 статей по запросу `"technology and innovation"` только среди статей с `topic = Tech`
2. Найдите топ-3 статей по запросу `"science discoveries"` только среди статей `year = 2023`
3. Найдите топ-3 статей по запросу `"sports championships"` среди статей с явным оператором `$ne`: исключите тему `Business`

**Ожидаемый результат:**
```
=== Только Tech ===
  1. New AI Model Outperforms Humans... (dist=0.XXXX)
  ...

=== Только 2023 год ===
  ...

=== Исключая Business ===
  ...
```

**Шаблон кода:**
```python
# Запрос 1: фильтр по topic
result = collection.query(
    query_texts=['technology and innovation'],
    n_results=3,
    where={'topic': 'Tech'}  # краткая форма $eq
)
print('=== Только Tech ===')
for doc, dist in zip(result['documents'][0], result['distances'][0]):
    print(f'  {doc[:50]}... (dist={dist:.4f})')

# Запрос 2: фильтр по году
result = collection.query(
    query_texts=['science discoveries'],
    n_results=3,
    where={'year': ...}
)
print('\n=== Только 2023 год ===')
...

# Запрос 3: оператор $ne
result = collection.query(
    query_texts=['sports championships'],
    n_results=3,
    where={'topic': {'$ne': 'Business'}}
)
print('\n=== Исключая Business ===')
...
```

### Задача 4.2: Комбинированные фильтры с $and и $or

**Что нужно сделать:**

1. Найдите статьи по запросу `"cutting edge technology"` с условием `$and`: тема `Tech` **И** год `2024`
2. Найдите статьи по запросу `"global events"` с условием `$or`: тема `Science` **ИЛИ** тема `Sport`
3. Выведите количество найденных результатов для каждого запроса

**Ожидаемый результат:**
```
=== Tech И 2024 год ===
Найдено: X результатов
  ...

=== Science ИЛИ Sport ===
Найдено: X результатов
  ...
```

**Шаблон кода:**
```python
# Фильтр $and
where_and = {
    '$and': [
        {'topic': {'$eq': ...}},
        {'year': {'$eq': ...}}
    ]
}

result = collection.query(
    query_texts=['cutting edge technology'],
    n_results=5,
    where=where_and
)
print('=== Tech И 2024 год ===')
print(f'Найдено: {len(result["documents"][0])} результатов')
...

# Фильтр $or
where_or = {
    '$or': [
        {'topic': {'$eq': ...}},
        {'topic': {'$eq': ...}}
    ]
}

result = collection.query(
    query_texts=['global events'],
    n_results=5,
    where=...
)
print('\n=== Science ИЛИ Sport ===')
...
```

---

## Часть 5: Рекомендательная система (20 минут)

### Задача 5.1: Рекомендации с фильтром по теме

**Сценарий:** Пользователь читает статью о криптовалюте. Система должна предложить похожие материалы, но **только из той же темы** (Business).

**Что нужно сделать:**

1. Получите текст статьи `art-02` из коллекции
2. Выполните запрос с `query_texts=[reference_text]` и фильтром `where={'topic': 'Business'}`
3. Из результатов исключите саму эталонную статью (`art-02`) в постобработке
4. Выведите финальные рекомендации

**Ожидаемый результат:**
```
Эталонная статья: "Bitcoin Reaches All-Time High as Investors Rush In"
Тема: Business

Рекомендации (только Business):
  1. Stock Markets Plunge Amid Recession Fears (dist=0.XXXX)
  2. Federal Reserve Raises Interest Rates Again (dist=0.XXXX)
```

**Шаблон кода:**
```python
reference_id = 'art-02'
reference_data = collection.get(ids=[reference_id])
reference_text = reference_data['documents'][0]
reference_topic = reference_data['metadatas'][0]['topic']

result = collection.query(
    query_texts=[reference_text],
    n_results=4,  # берём 4, чтобы после исключения эталона осталось 3
    where={'topic': reference_topic}
)

print(f'Эталонная статья: "{articles[1]["headline"]}"')
print(f'Тема: {reference_topic}\n')
print('Рекомендации (только Business):')
rank = 1
for doc_id, doc, dist in zip(result['ids'][0], result['documents'][0], result['distances'][0]):
    if doc_id == reference_id:
        continue  # исключаем эталонную статью
    print(f'  {rank}. {doc[:60]}... (dist={dist:.4f})')
    rank += 1
```

---

## Бонусное задание (необязательно, +20 минут)

### Задача 6: Очистка и пересоздание коллекции

**Что нужно сделать:**

1. Удалите коллекцию `news_articles` через `client_db.delete_collection('news_articles')`
2. Пересоздайте её заново
3. Загрузите данные батчами по 5 статей (используйте `upsert` в цикле)
4. Убедитесь, что итоговое количество документов равно 10
5. Выполните контрольный запрос и сравните результаты с Частью 2

**Шаблон кода:**
```python
# Удалите и пересоздайте коллекцию
client_db.delete_collection('news_articles')
collection = client_db.create_collection(
    name='news_articles',
    embedding_function=embedding_fn
)

# Загрузка батчами
batch_size = 5
for i in range(0, len(articles), batch_size):
    batch = articles[i:i + batch_size]
    collection.upsert(
        ids=...,
        documents=...,
        metadatas=...
    )
    print(f'Загружен батч {i // batch_size + 1}, документов в коллекции: {collection.count()}')

print(f'\nИтого документов: {collection.count()}')
```

---

## Критерии оценки

| Часть | Баллы | Критерий |
|-------|-------|----------|
| Часть 1 | 20 | Создание клиента, коллекции, оценка стоимости, загрузка данных с метаданными |
| Часть 2 | 20 | Семантический поиск, корректная работа с результатами (список списков) |
| Часть 3 | 15 | Корректное использование update/upsert/delete |
| Часть 4 | 25 | Фильтры where с простыми и комбинированными операторами |
| Часть 5 | 20 | Рекомендательная система с фильтром и постобработкой |
| Бонус | 20 | Пакетная загрузка, пересоздание коллекции |
| **Всего** | **100** | |

---

## Рекомендации по выполнению

1. **`get_collection` vs `create_collection`**: при получении существующей коллекции всегда передавайте `embedding_function` — без неё запросы `query` не смогут векторизовать текст
2. **Структура ответа `query`**: `result['documents']` — это **список списков**. Для одного запроса обращайтесь к `result['documents'][0]`, для N запросов — к `result['documents'][i]`
3. **`upsert` идемпотентен**: повторный вызов с теми же ID обновит данные, но не создаст дубликаты
4. **Метаданные должны быть компактными**: не храните полные тексты в метаданных — это замедляет работу
5. **Постобработка эталонов**: при рекомендациях «похожих на X» сама статья X всегда будет первой (расстояние ~0) — не забудьте её исключить

## Что вы освоите

После выполнения этого задания вы сможете:
- Создавать и управлять векторными коллекциями в ChromaDB
- Выполнять семантический поиск без ручного вычисления эмбеддингов
- Использовать метаданные для фильтрации результатов с операторами `$eq`, `$ne`, `$gt`, `$lt`, `$and`, `$or`
- Строить рекомендательные системы с тематической фильтрацией
- Оценивать стоимость операций эмбеддинга с помощью `tiktoken`

---

**Удачи в выполнении задания!**

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Vector_Databases_with_ChromaDB|Векторные базы данных с ChromaDB]]*
