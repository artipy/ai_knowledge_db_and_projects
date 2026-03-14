# Векторные базы данных с ChromaDB

Векторные базы данных решают ключевые проблемы хранения эмбеддингов в памяти: каждый вектор занимает ~13 КБ (1536 float-значений), пересчёт при каждом запросе нерентабелен, а линейный поиск по косинусному расстоянию не масштабируется. Для production-систем необходима специализированная векторная БД.

Связанные темы: [[OpenAI_API/Working_with_Embeddings]] · [[OpenAI_API/Embeddings_Applications]] · [[LLMOps/LLMOps_Overview]]

---

## Архитектура векторных баз данных

Типичный пайплайн приложения на эмбеддингах:
1. Документы → векторы → **сохраняются** в векторной БД
2. Запрос пользователя → вектор → **поиск** по БД
3. Результаты → пользователь

Векторные БД относятся к **NoSQL**-классу (ключ-значение, документные, графовые). Кроме эмбеддингов хранят исходные тексты и **метаданные** (ID, внешние ссылки, фильтруемые поля). Метаданные должны быть компактными — добавление больших текстов в метаданные снижает производительность.

### Выбор векторной БД

| Критерий | Варианты |
|---|---|
| Управление | Managed (SaaS) vs Self-hosted |
| Лицензия | Open-source vs Commercial |
| Архитектура | Под тип данных и сценарий |
| Функциональность | Мультимодальность, встроенные embeddings и др. |

В учебных целях используем **Chroma** — open-source, быстрая настройка.

---

## ChromaDB: основы

Chroma работает в двух режимах:
- **Локальный** — всё внутри Python-процесса (для разработки и прототипирования)
- **Клиент/сервер** — отдельный процесс сервера (для production)

### Создание клиента и коллекции

```python
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
import os

load_dotenv()

# Persistent client сохраняет файлы БД на диск
client_db = chromadb.PersistentClient(path='~/path/to/db')

# Функция эмбеддингов (можно использовать локальный LLM через LM Studio)
embedding_fn = OpenAIEmbeddingFunction(
    api_key=os.getenv('LOCAL_TOKEN'),
    model_name=os.getenv('LOCAL_MODEL'),
    api_base=os.getenv('LOCAL_URL')
)

# Создание коллекции (аналог таблицы в SQL)
collection = client_db.create_collection(
    name='my_collection',
    embedding_function=embedding_fn
)
```

Если функция эмбеддингов не указана — используется дефолтная.

---

## CRUD-операции

### Добавление документов

```python
# Одиночный документ
collection.add(ids=['doc-1'], documents=['Text of document'])

# Несколько документов
collection.add(
    ids=['doc-1', 'doc-2'],
    documents=['Text 1', 'Text 2']
)
```

Chroma автоматически генерирует эмбеддинги при вставке. ID нужно задавать вручную.

### Просмотр коллекции

```python
client_db.list_collections()   # все коллекции
collection.count()             # количество документов
collection.peek()              # первые 10 элементов (с эмбеддингами)
collection.get('doc-1')        # получить по ID (без эмбеддингов по умолчанию)
```

### Обновление и upsert

```python
# update — обновить существующие (новые эмбеддинги генерируются автоматически)
collection.update(
    ids=['id-1', 'id-2'],
    documents=['New document 1', 'New document 2']
)

# upsert — добавить если нет, обновить если есть
collection.upsert(
    ids=['id-3', 'id-4'],
    documents=['New doc 3', 'New doc 4']
)
```

### Удаление

```python
collection.delete(ids=['id-1', 'id-2'])  # удалить элементы
client_db.reset()                         # сбросить всю БД
```

---

## Запросы (Query)

Для поиска нужно получить коллекцию с той же функцией эмбеддингов, что при создании:

```python
collection = client_db.get_collection(
    name='netflix_titles',
    embedding_function=embedding_fn
)

result = collection.query(
    query_texts=['movies where people sing a lot'],
    n_results=3
)
```

### Структура ответа

Метод возвращает словарь с полями:
- `ids` — идентификаторы результатов
- `documents` — тексты документов
- `metadatas` — метаданные
- `distances` — метрики сходства
- `embeddings` — не возвращаются по умолчанию

Каждое поле содержит **список списков**: внешний список — по числу запросов, внутренний — результаты для каждого запроса.

### Несколько запросов одновременно

```python
# Получить эталонные тексты
reference_ids = ['s8170', 's8103']
reference_texts = collection.get(ids=reference_ids)['documents']

# Отправить все тексты как запросы
result = collection.query(
    query_texts=reference_texts,
    n_results=3
)
# Результат: 6 записей (3 на каждый запрос)
```

> Эталонные объекты попадут на первые места (максимальное сходство с собой). Их нужно отфильтровать в постобработке.

---

## Метаданные и фильтрация

### Добавление метаданных

```python
import csv

ids, metadatas = [], []

with open('netflix_titles.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ids.append(row['show_id'])
        metadatas.append({
            'type': row['type'],
            'release_year': int(row['release_year'])
        })

# Обновить коллекцию, добавив метаданные
collection.update(ids=ids, metadatas=metadatas)
```

### Фильтры where

```python
# Краткая форма (эквивалент $eq)
result = collection.query(
    query_texts=reference_texts,
    n_results=3,
    where={'type': 'Movie'}
)

# Явный оператор
where = {'type': {'$eq': 'Movie'}}
```

### Операторы сравнения

| Оператор | Значение |
|---|---|
| `$eq` | равно |
| `$ne` | не равно |
| `$gt` | больше |
| `$lt` | меньше |

### Логические операторы

```python
# AND: только фильмы после 2020 года
where = {
    '$and': [
        {'type': {'$eq': 'Movie'}},
        {'release_year': {'$gt': 2020}}
    ]
}

# OR: хотя бы одно условие
where = {
    '$or': [
        {'type': {'$eq': 'Movie'}},
        {'release_year': {'$gt': 2020}}
    ]
}
```

---

## Оценка стоимости эмбеддингов

Перед вставкой большого датасета стоит оценить стоимость с помощью `tiktoken`:

```python
import tiktoken

encoder = tiktoken.encoding_for_model('text-embedding-3-small')

total_tokens = sum(len(encoder.encode(text)) for text in documents)

cost_per_1k_tokens = 0.00002  # цена за 1000 токенов
cost = cost_per_1k_tokens * total_tokens / 1000

print(f'Total tokens: {total_tokens}')
print(f'Cost: ${cost:.4f}')
```

---

## Связанные темы

- [[OpenAI_API/Working_with_Embeddings]] — создание и работа с эмбеддингами
- [[OpenAI_API/Embeddings_Applications]] — семантический поиск, рекомендации, классификация
- [[LLMOps/LLMOps_Overview]] — RAG и векторные БД в контексте LLMOps
- [[Exercises/11_Vector_Databases_with_ChromaDB_Exercise]] — практическое задание по этой заметке
