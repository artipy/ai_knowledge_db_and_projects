# Практическое задание №10: Применение Embeddings

## Цель задания

Освоить практические применения эмбеддингов: построение обогащённых векторных представлений из нескольких признаков, реализацию семантического поиска, систем рекомендаций (на основе одной статьи и истории просмотров) и zero-shot классификации текста.

## Связанные материалы

- [[OpenAI_API/Embeddings_Applications|Применение Embeddings: поиск, рекомендации и классификация]]
- [[OpenAI_API/Working_with_Embeddings|Работа с Embeddings]]
- [[LLMOps/Development_Phase|Фаза разработки — RAG и векторные базы данных]]

## Следующие шаги

После выполнения этого задания вы сможете строить полноценные RAG-компоненты и рекомендательные системы. Это задание является продолжением [[Exercises/09_Working_with_Embeddings_Exercise|Практического задания №9]].

## Предварительные требования

- Выполненное задание №9 (понимание cosine distance и `create_embeddings`)
- Установленные библиотеки: `openai`, `python-dotenv`, `scipy`, `numpy`
- Настроенный `.env` файл с API ключом

```python
# Установка зависимостей
# pip install openai python-dotenv scipy numpy
```

---

## Исходные данные

Во всех частях задания используется следующий набор новостных статей:

```python
articles = [
    {"headline": "SpaceX Launches New Starship Rocket",
     "topic": "Science",
     "keywords": ["space", "rocket", "nasa", "exploration"]},
    {"headline": "Bitcoin Reaches All-Time High as Investors Rush In",
     "topic": "Business",
     "keywords": ["crypto", "bitcoin", "finance", "investment"]},
    {"headline": "Champions League Final: Real Madrid vs Manchester City",
     "topic": "Sport",
     "keywords": ["football", "soccer", "champions league", "madrid"]},
    {"headline": "New AI Model Outperforms Humans in Medical Diagnosis",
     "topic": "Tech",
     "keywords": ["ai", "healthcare", "machine learning", "diagnosis"]},
    {"headline": "Global Leaders Meet to Discuss Climate Change",
     "topic": "Science",
     "keywords": ["climate", "environment", "policy", "emissions"]},
    {"headline": "Apple Announces Revolutionary New iPhone",
     "topic": "Tech",
     "keywords": ["apple", "iphone", "smartphone", "technology"]},
    {"headline": "Stock Markets Plunge Amid Recession Fears",
     "topic": "Business",
     "keywords": ["stocks", "economy", "recession", "wall street"]},
    {"headline": "Olympics 2024: USA Wins Gold in Swimming",
     "topic": "Sport",
     "keywords": ["olympics", "swimming", "usa", "gold medal"]},
    {"headline": "Scientists Discover New Species in Amazon Rainforest",
     "topic": "Science",
     "keywords": ["biology", "amazon", "species", "nature"]},
    {"headline": "Tesla Unveils Autonomous Robot for Home Use",
     "topic": "Tech",
     "keywords": ["tesla", "robot", "automation", "ai"]},
    {"headline": "Federal Reserve Raises Interest Rates Again",
     "topic": "Business",
     "keywords": ["economy", "interest rates", "fed", "banking"]},
    {"headline": "NBA Finals: LeBron James Leads Team to Victory",
     "topic": "Sport",
     "keywords": ["basketball", "nba", "lebron", "finals"]},
]
```

---

## Часть 1: Обогащённые эмбеддинги (15 минут)

### Задача 1.1: Функция объединения признаков статьи

Вместо эмбеддинга только заголовка мы будем объединять заголовок, тему и ключевые слова в одну строку — это улучшает качество поиска.

**Что нужно сделать:**

1. Реализуйте функцию `create_article_text(article)`, которая возвращает строку формата:
```
Headline: <заголовок>
Topic: <тема>
Keywords: <ключевое слово 1>, <ключевое слово 2>, ...
```

2. Проверьте функцию, вызвав её для первой и последней статьи из `articles`

**Ожидаемый результат:**
```
Headline: SpaceX Launches New Starship Rocket
Topic: Science
Keywords: space, rocket, nasa, exploration

Headline: NBA Finals: LeBron James Leads Team to Victory
Topic: Sport
Keywords: basketball, nba, lebron, finals
```

**Шаблон кода:**
```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_TOKEN"),
    base_url=os.getenv("BASE_URL")
)

def create_embeddings(texts):
    response = client.embeddings.create(
        model=os.getenv("BASE_MODEL"),
        input=texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]

articles = [...]  # полный список выше

def create_article_text(article):
    # Ваш код здесь
    pass

# Проверка
print(create_article_text(articles[0]))
print()
print(create_article_text(articles[-1]))
```

### Задача 1.2: Создание обогащённых эмбеддингов для всех статей

**Что нужно сделать:**

Используя `create_article_text` и `create_embeddings`, создайте эмбеддинги для всех статей **одним запросом**.

**Ожидаемый результат:**
```
Создано эмбеддингов: 12
Длина каждого вектора: 1536
```

**Шаблон кода:**
```python
# Объедините признаки для каждой статьи с помощью list comprehension
article_texts = ...

# Создайте эмбеддинги одним запросом
article_embeddings = ...

print(f"Создано эмбеддингов: {len(article_embeddings)}")
print(f"Длина каждого вектора: {len(article_embeddings[0])}")
```

---

## Часть 2: Семантический поиск (20 минут)

### Задача 2.1: Реализация функции поиска N ближайших

**Что нужно сделать:**

Реализуйте функцию `find_n_closest(query_vector, embeddings, n=3)`, которая:
- Вычисляет косинусное расстояние от `query_vector` до каждого вектора в `embeddings`
- Возвращает список из `n` словарей `{'distance': ..., 'index': ...}`, отсортированных по возрастанию расстояния

**Шаблон кода:**
```python
from scipy.spatial import distance

def find_n_closest(query_vector: list, embeddings: list[list], n: int = 3):
    distances = []
    for i, embedding in enumerate(embeddings):
        dist = ...  # вычислите косинусное расстояние
        distances.append({'distance': dist, 'index': i})
    # Отсортируйте и верните n первых
    distances_sorted = ...
    return ...
```

### Задача 2.2: Поиск по запросу пользователя

**Что нужно сделать:**

Выполните семантический поиск по трём запросам. Для каждого запроса выведите топ-3 результата с заголовками и расстояниями.

**Поисковые запросы:**
```python
queries = [
    "artificial intelligence and technology",
    "financial markets and economy",
    "athletes and sports competitions",
]
```

**Ожидаемый результат:**
```
Запрос: "artificial intelligence and technology"
  1. New AI Model Outperforms Humans in Medical Diagnosis (dist=0.XXXX)
  2. Tesla Unveils Autonomous Robot for Home Use (dist=0.XXXX)
  3. Apple Announces Revolutionary New iPhone (dist=0.XXXX)

Запрос: "financial markets and economy"
  1. Stock Markets Plunge Amid Recession Fears (dist=0.XXXX)
  ...
```

**Шаблон кода:**
```python
queries = [
    "artificial intelligence and technology",
    "financial markets and economy",
    "athletes and sports competitions",
]

for query in queries:
    # Преобразуйте запрос в вектор
    query_vector = ...

    # Найдите 3 ближайших
    hits = find_n_closest(query_vector, article_embeddings)

    print(f'Запрос: "{query}"')
    for rank, hit in enumerate(hits, 1):
        article = articles[hit['index']]
        print(f"  {rank}. {article['headline']} (dist={hit['distance']:.4f})")
    print()
```

---

## Часть 3: Рекомендации по текущей статье (20 минут)

### Задача 3.1: Рекомендательная система на основе одной статьи

**Сценарий:** Пользователь читает статью о криптовалюте. Система должна предложить ему три похожих материала.

**Текущая статья:**
```python
current_article = {
    "headline": "Ethereum Surges 30% Following Network Upgrade",
    "topic": "Business",
    "keywords": ["ethereum", "crypto", "blockchain", "investment"]
}
```

**Что нужно сделать:**

1. Создайте обогащённый текст и эмбеддинг для `current_article`
2. Найдите 3 ближайшие статьи из `articles` с помощью `find_n_closest`
3. Выведите рекомендации с заголовками

**Ожидаемый результат:**
```
Статья: "Ethereum Surges 30% Following Network Upgrade"

Рекомендации:
  1. Bitcoin Reaches All-Time High as Investors Rush In (dist=0.XXXX)
  2. Federal Reserve Raises Interest Rates Again (dist=0.XXXX)
  3. Stock Markets Plunge Amid Recession Fears (dist=0.XXXX)
```

**Шаблон кода:**
```python
current_article = {
    "headline": "Ethereum Surges 30% Following Network Upgrade",
    "topic": "Business",
    "keywords": ["ethereum", "crypto", "blockchain", "investment"]
}

# Создайте текст и эмбеддинг текущей статьи
current_article_text = ...
current_article_embedding = ...

# Найдите похожие статьи
hits = find_n_closest(current_article_embedding, article_embeddings)

print(f'Статья: "{current_article["headline"]}"\n')
print("Рекомендации:")
for rank, hit in enumerate(hits, 1):
    article = articles[hit['index']]
    print(f"  {rank}. {article['headline']} (dist={hit['distance']:.4f})")
```

---

## Часть 4: Рекомендации на основе истории просмотров (25 минут)

### Задача 4.1: Усреднение эмбеддингов истории

**Сценарий:** Пользователь просмотрел две статьи о технологиях. Система должна порекомендовать ему похожие материалы, которые он ещё не читал.

**История просмотров пользователя:**
```python
user_history = [
    {"headline": "New AI Model Outperforms Humans in Medical Diagnosis",
     "topic": "Tech",
     "keywords": ["ai", "healthcare", "machine learning", "diagnosis"]},
    {"headline": "Apple Announces Revolutionary New iPhone",
     "topic": "Tech",
     "keywords": ["apple", "iphone", "smartphone", "technology"]},
]
```

**Что нужно сделать:**

1. Создайте обогащённые тексты и эмбеддинги для каждой статьи из `user_history`
2. Вычислите **среднее** всех эмбеддингов истории с помощью `np.mean(..., axis=0)` — это даст единый вектор предпочтений пользователя
3. Выведите размерность полученного среднего вектора

**Ожидаемый результат:**
```
Эмбеддингов в истории: 2
Размерность среднего вектора: 1536
```

**Шаблон кода:**
```python
import numpy as np

user_history = [...]

# Объедините признаки и создайте эмбеддинги истории
history_texts = ...
history_embeddings = ...

# Вычислите средний вектор
mean_history_embedding = ...

print(f"Эмбеддингов в истории: {len(history_embeddings)}")
print(f"Размерность среднего вектора: {len(mean_history_embedding)}")
```

### Задача 4.2: Фильтрация и рекомендации

**Что нужно сделать:**

1. Отфильтруйте из `articles` те статьи, которые уже есть в `user_history`
2. Создайте эмбеддинги для оставшихся (непросмотренных) статей
3. Найдите топ-3 рекомендации на основе среднего вектора истории
4. Выведите результаты

> **Подсказка:** Для фильтрации используйте list comprehension с условием `if article not in user_history`

**Ожидаемый результат:**
```
Статей в каталоге: 12
Статей после фильтрации: 10

Рекомендации (на основе истории):
  1. Tesla Unveils Autonomous Robot for Home Use (dist=0.XXXX)
  2. New AI Model Outperforms Humans in Medical Diagnosis — уже просмотрена, не должна появиться
  3. ...
```

**Шаблон кода:**
```python
# Отфильтруйте просмотренные статьи
articles_filtered = [article for article in articles if ...]

print(f"Статей в каталоге: {len(articles)}")
print(f"Статей после фильтрации: {len(articles_filtered)}")

# Создайте тексты и эмбеддинги для непросмотренных статей
filtered_texts = ...
filtered_embeddings = ...

# Найдите рекомендации по среднему вектору истории
hits = find_n_closest(mean_history_embedding, filtered_embeddings)

print("\nРекомендации (на основе истории):")
for rank, hit in enumerate(hits, 1):
    article = articles_filtered[hit['index']]
    print(f"  {rank}. {article['headline']} (dist={hit['distance']:.4f})")
```

---

## Часть 5: Zero-Shot классификация (20 минут)

### Задача 5.1: Классификация с короткими метками

**Что нужно сделать:**

1. Реализуйте функцию `find_closest(query_vector, embeddings)`, которая возвращает единственный ближайший результат (словарь `{'index': ..., 'distance': ...}`) без сортировки — используйте `min()`
2. Определите классы и их метки:
```python
topics = [
    {'label': 'Tech'},
    {'label': 'Science'},
    {'label': 'Sport'},
    {'label': 'Business'}
]
```
3. Классифицируйте следующие статьи, используя в качестве описаний классов только сами метки (`label`):

```python
test_articles = [
    {"headline": "Quantum Computing Breakthrough Could Revolutionize Cryptography",
     "keywords": ["quantum", "computing", "encryption", "technology"]},
    {"headline": "Marathon World Record Broken at Berlin Race",
     "keywords": ["running", "marathon", "athletics", "world record"]},
    {"headline": "Startup Raises $500M to Build Nuclear Fusion Reactor",
     "keywords": ["energy", "nuclear", "startup", "investment"]},
]
```

4. Выведите результат классификации для каждой статьи

**Шаблон кода:**
```python
def find_closest(query_vector, embeddings):
    distances = []
    for i, emb in enumerate(embeddings):
        dist = distance.cosine(query_vector, emb)
        distances.append({'index': i, 'distance': dist})
    return min(distances, key=lambda x: x['distance'])

def create_article_text_for_classification(article):
    return f'''Headline: {article['headline']}
Keywords: {', '.join(article['keywords'])}'''

topics = [
    {'label': 'Tech'},
    {'label': 'Science'},
    {'label': 'Sport'},
    {'label': 'Business'}
]

test_articles = [...]

# Создайте эмбеддинги меток
class_descriptions = [topic['label'] for topic in topics]
class_embeddings = ...

print("=== Классификация с короткими метками ===")
for article in test_articles:
    article_text = create_article_text_for_classification(article)
    article_embedding = create_embeddings(article_text)[0]
    closest = find_closest(article_embedding, class_embeddings)
    label = topics[closest['index']]['label']
    print(f'"{article["headline"]}" → {label}')
```

### Задача 5.2: Улучшение классификации с развёрнутыми описаниями

**Что нужно сделать:**

1. Дополните словари `topics` полем `description` с развёрнутым описанием каждого класса
2. Повторите классификацию из Задачи 5.1, используя теперь `description` вместо `label`
3. Сравните результаты двух подходов: изменились ли метки? Стали ли они точнее?

**Примерные описания (можно доработать):**
```python
topics = [
    {'label': 'Tech',     'description': 'A news article about technology, gadgets, software or digital innovation'},
    {'label': 'Science',  'description': 'A news article about scientific research, discoveries or natural phenomena'},
    {'label': 'Sport',    'description': 'A news article about sports, athletes, competitions or championships'},
    {'label': 'Business', 'description': 'A news article about economy, finance, markets or investments'}
]
```

**Ожидаемый результат:**
```
=== Классификация с развёрнутыми описаниями ===
"Quantum Computing Breakthrough Could Revolutionize Cryptography" → Tech
"Marathon World Record Broken at Berlin Race" → Sport
"Startup Raises $500M to Build Nuclear Fusion Reactor" → Science  (или Business — обсудите почему)

=== Сравнение ===
Метки совпали: X из 3
```

**Шаблон кода:**
```python
topics = [
    {'label': 'Tech',     'description': '...'},
    {'label': 'Science',  'description': '...'},
    {'label': 'Sport',    'description': '...'},
    {'label': 'Business', 'description': '...'}
]

# Создайте эмбеддинги описаний
class_descriptions = [topic['description'] for topic in topics]
class_embeddings = ...

labels_with_descriptions = []

print("=== Классификация с развёрнутыми описаниями ===")
for article in test_articles:
    article_text = create_article_text_for_classification(article)
    article_embedding = create_embeddings(article_text)[0]
    closest = find_closest(article_embedding, class_embeddings)
    label = topics[closest['index']]['label']
    labels_with_descriptions.append(label)
    print(f'"{article["headline"]}" → {label}')
```

---

## Бонусное задание (необязательно, +20 минут)

### Задача 6: Полный пайплайн — персонализированная лента с классификацией

**Сценарий:** Объедините все изученные техники в один пайплайн. Пользователь читает статью, система:
1. Классифицирует её по теме
2. Рекомендует 3 похожие статьи с той же темой

**Что нужно сделать:**

1. Напишите функцию `classify_article(article, topics)`, которая возвращает метку темы для переданной статьи (используйте `find_closest` с развёрнутыми описаниями)
2. Напишите функцию `recommend_by_topic(article, articles, n=3)`, которая:
   - Классифицирует `article`
   - Фильтрует `articles`, оставляя только те, что имеют такую же тему (`topic`)
   - Возвращает топ-N наиболее похожих по эмбеддингу
3. Протестируйте на `current_article` из Части 3

**Ожидаемый результат:**
```
Статья: "Ethereum Surges 30% Following Network Upgrade"
Определённая тема: Business

Рекомендации в теме Business:
  1. Bitcoin Reaches All-Time High as Investors Rush In (dist=0.XXXX)
  2. Stock Markets Plunge Amid Recession Fears (dist=0.XXXX)
  3. Federal Reserve Raises Interest Rates Again (dist=0.XXXX)
```

---

## Критерии оценки

| Часть | Баллы | Критерий |
|-------|-------|----------|
| Часть 1 | 10 | Корректная функция `create_article_text` и пакетное создание эмбеддингов |
| Часть 2 | 20 | Реализация `find_n_closest` и семантический поиск с корректными результатами |
| Часть 3 | 20 | Рекомендации по текущей статье через обогащённый эмбеддинг |
| Часть 4 | 25 | Усреднение истории, правильная фильтрация просмотренных статей, корректные рекомендации |
| Часть 5 | 25 | Реализация `find_closest`, классификация с метками и описаниями, сравнительный анализ |
| Бонус | 20 | Работающий пайплайн с классификацией и тематической фильтрацией рекомендаций |
| **Всего** | **100** | |

## Рекомендации по выполнению

1. **Порядок имеет значение**: `create_article_text` из Части 1 используется во всех последующих частях — убедитесь, что функция работает корректно
2. **Один запрос для батча**: при создании эмбеддингов передавайте весь список текстов за один вызов `create_embeddings`, а не в цикле
3. **Сохраняйте эмбеддинги**: не пересоздавайте `article_embeddings` в каждой части — переиспользуйте переменную из Части 1
4. **Часть 4 — тонкость**: после фильтрации статей `articles_filtered` индексы в результатах `find_n_closest` указывают на позиции в `articles_filtered`, а не в исходном `articles`
5. **Часть 5 — обсудите результаты**: некоторые статьи могут классифицироваться неоднозначно (например, «стартап привлёк инвестиции на строительство реактора» — Tech, Science или Business?) — это нормально, опишите ваши наблюдения в комментарии

## Что вы освоите

После выполнения этого задания вы сможете:
- Строить обогащённые векторные представления из нескольких текстовых признаков
- Реализовывать семантический поиск с функцией поиска N ближайших соседей
- Строить рекомендательные системы на основе одного элемента и истории просмотров
- Агрегировать несколько эмбеддингов в один вектор предпочтений через усреднение
- Применять zero-shot классификацию и понимать влияние качества описаний классов на точность

---

**Удачи в выполнении задания!**

*Если возникнут вопросы, обратитесь к материалам [[OpenAI_API/Embeddings_Applications|Применение Embeddings: поиск, рекомендации и классификация]]*
