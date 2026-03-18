# Практическое задание №13: Операции с векторами в Pinecone

## Цель задания

Освоить полный цикл работы с векторами в Pinecone: получение записей по ID (fetch), семантический поиск с настройкой метрик расстояния (query), фильтрацию по метаданным с операторами сравнения, обновление значений векторов и метаданных, а также удаление записей по ID, по фильтру и очистку пространств имён.

## Связанные материалы

- [[OpenAI_API/Pinecone_Vector_Manipulation|Операции с векторами в Pinecone]]
- [[OpenAI_API/Vector_Databases_with_Pinecone|Векторные базы данных с Pinecone]]
- [[OpenAI_API/Working_with_Embeddings|Работа с Embeddings]]
- [[OpenAI_API/Embeddings_Applications|Применение Embeddings: поиск, рекомендации и классификация]]

## Следующие шаги

Это задание является продолжением [[Exercises/12_Vector_Databases_with_Pinecone_Exercise|Практического задания №12]]. После выполнения вы освоите полный CRUD-цикл работы с векторами в Pinecone и сможете строить приложения с семантическим поиском и управлением данными.

## Предварительные требования

- Выполненное задание №12 (создание индекса, upsert, базовый поиск)
- Учётная запись Pinecone (бесплатный план Starter на [pinecone.io](https://pinecone.io))
- Настроенный `.env` файл с ключами `PINE_API` и `OPENAI_API_KEY`
- Установленные библиотеки: `pinecone`, `openai`, `python-dotenv`

```python
# pip install pinecone openai python-dotenv
```

---

## Подготовка: данные и настройка индекса

Во всех частях задания используется тот же набор новостных статей. Перед выполнением частей 2–5 необходимо создать индекс и загрузить данные.

```python
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINE_API'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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

def create_article_text(article):
    keywords_str = ', '.join(article['keywords'])
    return f"Headline: {article['headline']}\nTopic: {article['topic']}\nKeywords: {keywords_str}"

# Создайте индекс и загрузите данные перед выполнением заданий
INDEX_NAME = 'manipulation-index'

pc.create_index(
    name=INDEX_NAME,
    dimension=1536,
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)

index = pc.Index(INDEX_NAME)

article_texts = [create_article_text(a) for a in articles]
response = client.embeddings.create(input=article_texts, model='text-embedding-3-small')

vectors = [
    {
        'id': articles[i]['id'],
        'values': response.data[i].embedding,
        'metadata': {'topic': articles[i]['topic'], 'year': articles[i]['year']}
    }
    for i in range(len(articles))
]

index.upsert(vectors=vectors)
print('Данные загружены. Векторов:', len(vectors))
```

---

## Часть 1: Получение векторов (Fetch)

### Задача 1.1: Получение записей по ID

**Что нужно сделать:**

1. Вызовите `index.fetch()`, передав список ID `['art-01', 'art-04']`
2. Из ответа извлеките и выведите для каждой записи: ID, первые 5 значений вектора и метаданные
3. Выведите количество потреблённых Read Units из поля `'usage'`

**Ожидаемый результат:**
```
art-01 | topic=Science, year=2024 | vector[:5]=[0.0123, ...]
art-04 | topic=Tech, year=2024 | vector[:5]=[0.0456, ...]
Read Units: 1
```

**Шаблон кода:**
```python
fetch_result = index.fetch(ids=['art-01', 'art-04'])

for record_id, record in fetch_result['vectors'].items():
    values_preview = record['values'][:5]
    metadata = record['metadata']
    print(f"{record_id} | topic={metadata['topic']}, year={metadata['year']} | vector[:5]={[round(v, 4) for v in values_preview]}")

# Ваш код здесь: выведите fetch_result['usage']
```

### Задача 1.2: Fetch из несуществующего namespace

**Что нужно сделать:**

1. Вызовите `index.fetch()` с теми же ID, но указав `namespace='nonexistent-ns'`
2. Выведите результат и объясните в комментарии, что возвращает Pinecone, если namespace не существует

**Шаблон кода:**
```python
result = index.fetch(
    ids=['art-01', 'art-04'],
    namespace=...  # несуществующий namespace
)

print(result)
# Почему result['vectors'] пустой? # Ваш комментарий здесь
```

---

## Часть 2: Запросы к векторам (Query)

### Задача 2.1: Базовый семантический поиск

**Что нужно сделать:**

1. Создайте эмбеддинг для запроса `"space exploration and rockets"`
2. Выполните запрос к индексу с `top_k=3`
3. Выведите ID и score для каждого результата
4. Убедитесь, что `art-01` (SpaceX) находится в топ-1

**Ожидаемый результат:**
```
Запрос: "space exploration and rockets"
  1. art-01 | score=0.XXXX
  2. art-05 | score=0.XXXX
  3. art-09 | score=0.XXXX
```

**Шаблон кода:**
```python
query_text = "space exploration and rockets"

query_vector = client.embeddings.create(
    input=[query_text],
    model='text-embedding-3-small'
).data[0].embedding

result = index.query(
    vector=...,
    top_k=...
)

print(f'Запрос: "{query_text}"')
for i, match in enumerate(result['matches'], 1):
    print(f"  {i}. {match['id']} | score={match['score']:.4f}")
```

### Задача 2.2: Запрос с возвратом значений вектора

**Что нужно сделать:**

1. Повторите запрос из задачи 2.1, добавив `include_values=True`
2. Для первого результата выведите первые 5 значений вектора
3. В комментарии объясните: в каком случае полезен параметр `include_values`

**Шаблон кода:**
```python
result = index.query(
    vector=query_vector,
    top_k=3,
    include_values=...
)

top_match = result['matches'][0]
print(f"ID: {top_match['id']}")
print(f"Score: {top_match['score']:.4f}")
print(f"Vector[:5]: {[round(v, 4) for v in top_match['values'][:5]]}")
# Когда нужен include_values=True? # Ваш комментарий здесь
```

### Задача 2.3: Создание индекса с другой метрикой

**Что нужно сделать:**

1. Создайте **новый** индекс `'dotproduct-index'` с метрикой `'dotproduct'` и той же размерностью `1536`
2. Загрузите в него те же 10 векторов
3. Выполните тот же запрос `"space exploration and rockets"` с `top_k=3`
4. Сравните порядок результатов и значения score с результатами из задачи 2.1
5. Объясните в комментарии: почему score из `dotproduct`-индекса и `cosine`-индекса нельзя сравнивать напрямую

**Шаблон кода:**
```python
pc.create_index(
    name='dotproduct-index',
    dimension=1536,
    metric=...,
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)

dp_index = pc.Index('dotproduct-index')
dp_index.upsert(vectors=vectors)

dp_result = dp_index.query(
    vector=query_vector,
    top_k=3
)

print('=== cosine ===')
for m in result['matches']:
    print(f"  {m['id']} | score={m['score']:.4f}")

print('\n=== dotproduct ===')
for m in dp_result['matches']:
    print(f"  {m['id']} | score={m['score']:.4f}")

# Чем отличаются метрики и почему score нельзя сравнивать напрямую?
# Ваш комментарий здесь
```

> **Важно:** По завершении задачи 2.3 удалите `dotproduct-index`:
> ```python
> pc.delete_index('dotproduct-index')
> ```

---

## Часть 3: Фильтрация по метаданным

### Задача 3.1: Фильтр по точному значению ($eq)

**Что нужно сделать:**

1. Запрос: `"innovation and new technologies"`, `top_k=3`, фильтр `topic = 'Tech'`
2. Запрос: `"environmental issues"`, `top_k=3`, фильтр `year = 2023`
3. Для каждого запроса выведите ID, score и метаданные. Убедитесь, что все результаты соответствуют фильтру

**Ожидаемый результат:**
```
=== Только Tech ===
  art-04 | score=0.XXXX | topic=Tech, year=2024
  art-06 | score=0.XXXX | topic=Tech, year=2024
  art-10 | score=0.XXXX | topic=Tech, year=2024

=== Только 2023 год ===
  art-05 | score=0.XXXX | topic=Science, year=2023
  ...
```

**Шаблон кода:**
```python
# Запрос 1: фильтр по topic
q1_vector = client.embeddings.create(
    input=['innovation and new technologies'],
    model='text-embedding-3-small'
).data[0].embedding

result1 = index.query(
    vector=q1_vector,
    top_k=3,
    include_metadata=True,
    filter={'topic': {'$eq': ...}}
)

print('=== Только Tech ===')
for match in result1['matches']:
    print(f"  {match['id']} | score={match['score']:.4f} | topic={match['metadata']['topic']}, year={match['metadata']['year']}")

# Запрос 2: фильтр по году
q2_vector = client.embeddings.create(
    input=['environmental issues'],
    model='text-embedding-3-small'
).data[0].embedding

result2 = index.query(
    vector=q2_vector,
    top_k=3,
    include_metadata=True,
    filter={'year': ...}  # краткая форма для равенства
)

print('\n=== Только 2023 год ===')
for match in result2['matches']:
    print(f"  {match['id']} | score={match['score']:.4f} | topic={match['metadata']['topic']}, year={match['metadata']['year']}")
```

### Задача 3.2: Операторы сравнения ($gt, $ne)

**Что нужно сделать:**

1. Запрос: `"sports competitions"`, `top_k=3`, фильтр `year > 2023`
2. Запрос: `"financial markets"`, `top_k=5`, фильтр `topic ≠ 'Business'`
3. Убедитесь, что результаты соответствуют условиям фильтрации

**Шаблон кода:**
```python
# Запрос 1: год строго больше 2023
q3_vector = client.embeddings.create(
    input=['sports competitions'],
    model='text-embedding-3-small'
).data[0].embedding

result3 = index.query(
    vector=q3_vector,
    top_k=3,
    include_metadata=True,
    filter={'year': {'$gt': ...}}
)

print('=== год > 2023 ===')
for match in result3['matches']:
    print(f"  {match['id']} | year={match['metadata']['year']}")

# Запрос 2: исключить Business
q4_vector = client.embeddings.create(
    input=['financial markets'],
    model='text-embedding-3-small'
).data[0].embedding

result4 = index.query(
    vector=q4_vector,
    top_k=5,
    include_metadata=True,
    filter={'topic': {'$ne': ...}}
)

print('\n=== Исключить Business ===')
for match in result4['matches']:
    print(f"  {match['id']} | topic={match['metadata']['topic']}")
```

### Задача 3.3: Комбинированный фильтр

**Что нужно сделать:**

Выполните поиск по запросу `"breakthrough discoveries"` с `top_k=5`, применив оба условия одновременно: `topic = 'Science'` **И** `year = 2023`.

> **Подсказка:** Для комбинирования нескольких условий передайте их в один словарь `filter` несколькими ключами.

**Ожидаемый результат:**
```
=== Science И 2023 год ===
  art-05 | topic=Science, year=2023
  art-09 | topic=Science, year=2023
```

**Шаблон кода:**
```python
q5_vector = client.embeddings.create(
    input=['breakthrough discoveries'],
    model='text-embedding-3-small'
).data[0].embedding

result5 = index.query(
    vector=q5_vector,
    top_k=5,
    include_metadata=True,
    filter={
        'topic': ...,   # Science
        'year': ...     # 2023
    }
)

print('=== Science И 2023 год ===')
for match in result5['matches']:
    print(f"  {match['id']} | topic={match['metadata']['topic']}, year={match['metadata']['year']}")
```

---

## Часть 4: Обновление векторов

### Задача 4.1: Обновление значений вектора

**Что нужно сделать:**

1. Получите текущие данные записи `art-07` через `fetch`
2. Создайте новый эмбеддинг для изменённого текста:
   ```
   Headline: Stock Markets Rally Following Fed Rate Cut
   Topic: Business
   Keywords: stocks, economy, federal reserve, recovery
   ```
3. Обновите вектор `art-07` новым значением через `index.update()`
4. Снова получите запись через `fetch` и убедитесь, что первые 5 значений вектора изменились

**Ожидаемый результат:**
```
До обновления: vector[:5]=[0.XXXX, ...]
После обновления: vector[:5]=[0.YYYY, ...]  ← значения изменились
```

**Шаблон кода:**
```python
# Получите текущие данные
before = index.fetch(ids=['art-07'])
before_values = before['vectors']['art-07']['values'][:5]
print(f"До обновления: vector[:5]={[round(v, 4) for v in before_values]}")

# Создайте новый эмбеддинг
new_text = "Headline: Stock Markets Rally Following Fed Rate Cut\nTopic: Business\nKeywords: stocks, economy, federal reserve, recovery"
new_vector = client.embeddings.create(
    input=[new_text],
    model='text-embedding-3-small'
).data[0].embedding

# Обновите вектор
index.update(id=..., values=...)

# Проверьте обновление
after = index.fetch(ids=['art-07'])
after_values = after['vectors']['art-07']['values'][:5]
print(f"После обновления: vector[:5]={[round(v, 4) for v in after_values]}")
```

### Задача 4.2: Обновление метаданных

**Что нужно сделать:**

1. Обновите метаданные записи `art-07`: добавьте поле `rating=4` и измените `year` на `2024`
2. Получите запись через `fetch` и убедитесь, что:
   - `rating` появился в метаданных
   - `year` изменился на `2024`
   - `topic` остался прежним (`Business`)

**Шаблон кода:**
```python
index.update(
    id='art-07',
    set_metadata={...}  # rating=4, year=2024
)

updated = index.fetch(ids=['art-07'])
metadata = updated['vectors']['art-07']['metadata']
print(f"topic: {metadata['topic']}")   # ожидается 'Business' (без изменений)
print(f"year: {metadata['year']}")     # ожидается 2024
print(f"rating: {metadata['rating']}") # ожидается 4
```

### Задача 4.3: Одновременное обновление вектора и метаданных

**Что нужно сделать:**

Обновите `art-03` за один вызов `index.update()`: установите новый вектор (эмбеддинг из строки `"Football final match 2024"`) и одновременно обновите метаданные: `year=2024`, добавьте `rating=5`.

**Шаблон кода:**
```python
new_vec = client.embeddings.create(
    input=['Football final match 2024'],
    model='text-embedding-3-small'
).data[0].embedding

index.update(
    id='art-03',
    values=...,
    set_metadata=...
)

result = index.fetch(ids=['art-03'])
print(result['vectors']['art-03']['metadata'])
```

---

## Часть 5: Удаление векторов

### Задача 5.1: Удаление по ID

**Что нужно сделать:**

1. Выведите текущее количество векторов в индексе через `describe_index_stats()`
2. Удалите записи `art-09` и `art-10` по ID через `index.delete()`
3. Снова вызовите `describe_index_stats()` и убедитесь, что количество уменьшилось на 2
4. Попробуйте получить удалённую запись через `fetch` — объясните в комментарии, что возвращает Pinecone

**Ожидаемый результат:**
```
До удаления: 10
После удаления: 8
fetch удалённой записи: vectors={}
```

**Шаблон кода:**
```python
stats_before = index.describe_index_stats()
print(f"До удаления: {stats_before['total_vector_count']}")

index.delete(ids=[..., ...])  # art-09, art-10

stats_after = index.describe_index_stats()
print(f"После удаления: {stats_after['total_vector_count']}")

fetch_deleted = index.fetch(ids=['art-09'])
print(f"fetch удалённой записи: vectors={fetch_deleted['vectors']}")
# Что вернул Pinecone? # Ваш комментарий здесь
```

### Задача 5.2: Удаление по фильтру метаданных

**Что нужно сделать:**

1. Выведите текущее количество векторов
2. Удалите все записи, у которых `topic = 'Sport'` — используйте `index.delete(filter=...)`
3. Убедитесь, что `art-03` и `art-08` удалены: попробуйте их получить через `fetch`
4. Проверьте итоговое количество векторов

> **Важно:** Функциональность удаления по фильтру доступна только в pod-based индексах или в serverless-индексах с планом выше Starter. Если получаете ошибку — выполните удаление по ID: `index.delete(ids=['art-03', 'art-08'])`.

**Шаблон кода:**
```python
stats = index.describe_index_stats()
print(f"До удаления Sport: {stats['total_vector_count']}")

try:
    index.delete(filter={'topic': {'$eq': ...}})
except Exception as e:
    print(f"Фильтрация при удалении недоступна: {e}")
    # Запасной вариант: удаление по ID
    index.delete(ids=['art-03', 'art-08'])

fetch_sport = index.fetch(ids=['art-03', 'art-08'])
print(f"Запрошено: 2, получено: {len(fetch_sport['vectors'])}")  # ожидается 0

stats = index.describe_index_stats()
print(f"После удаления Sport: {stats['total_vector_count']}")
```

---

## Бонусное задание (необязательно)

### Задача 6: CRUD-цикл с пространствами имён

**Сценарий:** Вы реализуете систему разделения данных по темам. Каждый тип новостей хранится в своём namespace, что позволяет обновлять данные одной темы независимо от других.

**Что нужно сделать:**

1. Загрузите все 10 оригинальных статей в `namespace='archive-2023'` — только те, где `year=2023`
2. Загрузите статьи `year=2024` в `namespace='live-2024'`
3. Вызовите `describe_index_stats()` — убедитесь, что оба namespace отображаются
4. Выполните поиск `"ai technology"` с `top_k=3` **только в `live-2024`**
5. Очистите `archive-2023` через `index.delete(delete_all=True, namespace='archive-2023')`
6. Убедитесь через `describe_index_stats()`, что namespace `archive-2023` исчез из статистики

**Шаблон кода:**
```python
archive_vectors = [v for v, a in zip(vectors, articles) if a['year'] == 2023]
live_vectors = [v for v, a in zip(vectors, articles) if a['year'] == 2024]

index.upsert(vectors=archive_vectors, namespace=...)
index.upsert(vectors=live_vectors, namespace=...)

print('Namespaces:', index.describe_index_stats()['namespaces'])

ai_vector = client.embeddings.create(
    input=['ai technology'],
    model='text-embedding-3-small'
).data[0].embedding

result = index.query(
    vector=ai_vector,
    top_k=3,
    include_metadata=True,
    namespace=...
)

print('\nРезультаты в live-2024:')
for match in result['matches']:
    print(f"  {match['id']} | score={match['score']:.4f} | year={match['metadata']['year']}")

# Очистите archive-2023
index.delete(delete_all=True, namespace=...)

print('\nПосле очистки archive-2023:')
print(index.describe_index_stats()['namespaces'])
```

---

## Очистка (обязательно выполнить в конце)

```python
pc.delete_index('manipulation-index')
print('Индекс удалён.')
print('Оставшиеся индексы:', pc.list_indexes())
```

> **Важно:** На бесплатном плане Pinecone ограниченное количество индексов. Всегда удаляйте тестовые индексы по завершении работы.

---

## Критерии оценки

| Часть | Баллы | Критерий |
|---|---|---|
| Часть 1 | 10 | Fetch по ID, вывод данных записи, обработка несуществующего namespace |
| Часть 2 | 20 | Базовый query, include_values, создание и сравнение индексов с разными метриками |
| Часть 3 | 25 | Фильтры $eq, $gt, $ne, комбинированный фильтр с двумя условиями |
| Часть 4 | 25 | Обновление вектора, обновление метаданных, одновременное обновление |
| Часть 5 | 20 | Удаление по ID, удаление по фильтру, поведение fetch для удалённых записей |
| Бонус | 20 | CRUD-цикл с namespaces: загрузка, поиск, очистка namespace |
| **Всего** | **100** | |

---

## Рекомендации по выполнению

1. **Fetch vs Query**: `fetch` возвращает конкретные записи по ID; `query` ищет наиболее семантически близкие векторы — это разные операции для разных задач
2. **Read Units (RU)**: и `fetch`, и `query` расходуют RU; для `fetch` — 1 RU за 10 записей; для `query` — зависит от числа векторов и их размера
3. **Метрики расстояния**: задаются при создании индекса и не изменяются после. Score из `cosine` и `dotproduct` индексов имеют разную природу и не сравнимы напрямую
4. **set_metadata частичное**: `index.update(set_metadata=...)` обновляет только указанные поля; остальные поля метаданных сохраняются без изменений
5. **Задержка обновления**: после `update` и `delete` статистика индекса обновляется с небольшой задержкой — это нормальное поведение
6. **fetch несуществующих**: если запись не найдена (удалена или ID не существует), `fetch` возвращает пустой словарь `'vectors': {}`, а не ошибку

## Что вы освоите

После выполнения этого задания вы сможете:
- Получать конкретные записи по ID с помощью `fetch` и анализировать потребление Read Units
- Выполнять семантический поиск с настройкой `top_k`, `include_values`, `include_metadata`
- Выбирать подходящую метрику расстояния при создании индекса
- Применять фильтры метаданных с операторами `$eq`, `$gt`, `$ne` и их комбинациями
- Обновлять значения векторов и метаданные через `index.update()` и `set_metadata`
- Удалять записи по ID, по фильтру и очищать пространства имён

---

**Удачи в выполнении задания!**

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Pinecone_Vector_Manipulation|Операции с векторами в Pinecone]]*
