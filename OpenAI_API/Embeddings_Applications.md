# Применение Embeddings: поиск, рекомендации и классификация

Embeddings открывают широкий спектр практических применений: семантический поиск, системы рекомендаций и zero-shot классификация. Все три задачи используют одну и ту же механику — вычисление косинусного расстояния между векторами.

## Обогащённые эмбеддинги (Enriched Embeddings)

Вместо того чтобы создавать эмбеддинг только для текста заголовка, можно **объединить несколько признаков** в одну строку. Это повышает качество поиска и рекомендаций.

```python
articles = [
    {"headline": "Economic Growth Continues Amid Global Uncertainty",
     "topic": "Business",
     "keywords": ["economy", "business", "finance"]},
    # ...
    {"headline": "1.5 Billion Tune-in to the World Cup Final",
     "topic": "Sport",
     "keywords": ["soccer", "world cup", "tv"]}
]

def create_article_text(article):
    return f'''Headline: {article['headline']}
Topic: {article['topic']}
Keywords: {', '.join(article['keywords'])}'''
```

Функция использует f-строку с тройными кавычками для многострочного текста. Метод `join` преобразует список ключевых слов в строку через запятую.

```python
article_texts = [create_article_text(article) for article in articles]
article_embeddings = create_embeddings(article_texts)
```

---

## Семантический поиск

Процесс состоит из трёх шагов:
1. Преобразовать запрос и тексты в эмбеддинги
2. Вычислить косинусное расстояние между вектором запроса и остальными
3. Вернуть тексты с наименьшим расстоянием

### Функция поиска N ближайших результатов

```python
from scipy.spatial import distance

def find_n_closest(query_vector: list, embeddings: list[list], n: int = 3):
    distances = []
    for i, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({'distance': dist, 'index': i})
    distances_sorted = sorted(distances, key=lambda x: x['distance'])
    return distances_sorted[:n]
```

### Выполнение поиска

```python
query_text = 'AI'
query_vector = create_embeddings(query_text)[0]

hits = find_n_closest(query_vector, article_embeddings)

for hit in hits:
    article = articles[hit['index']]
    print(article['headline'])
```

---

## Система рекомендаций

Рекомендательная система работает почти так же, как семантический поиск — разница лишь в том, что «запросом» служит сама текущая статья (или история просмотров пользователя).

### Рекомендации по текущей статье

```python
current_article = {
    "headline": "How NVIDIA GPUs Could Decide Who Wins the AI Race",
    "topic": "Tech",
    "keywords": ["ai", "business", "computers"]
}

current_article_text = create_article_text(current_article)
current_article_embedding = create_embeddings(current_article_text)[0]
article_embeddings = create_embeddings(article_texts)

hits = find_n_closest(current_article_embedding, article_embeddings)

for hit in hits:
    article = articles[hit['index']]
    print(article['headline'])
```

### Рекомендации на основе истории просмотров

Если пользователь просмотрел несколько статей, нужно **усреднить их эмбеддинги** — это даёт вектор, близкий сразу к нескольким точкам данных.

```python
import numpy as np

user_history = [
    {"headline": "How NVIDIA GPUs Could Decide Who Wins the AI Race",
     "topic": "Tech",
     "keywords": ["ai", "business", "computers"]},
    {"headline": "Tech Giant Buys 49% Stake In AI Startup",
     "topic": "Tech",
     "keywords": ["business", "AI"]}
]

# Создаём усреднённый вектор из истории
history_texts = [create_article_text(item) for item in user_history]
history_embeddings = create_embeddings(history_texts)
mean_history_embedding = np.mean(history_embeddings, axis=0)

# Фильтруем уже просмотренные статьи
article_filtered = [article for article in articles if article not in user_history]
article_texts_filtered = [create_article_text(article) for article in article_filtered]
article_embeddings_filtered = create_embeddings(article_texts_filtered)

hits = find_n_closest(mean_history_embedding, article_embeddings_filtered)

for hit in hits:
    article = article_filtered[hit['index']]
    print(article['headline'])
```

> **Важно:** Фильтрация просмотренных статей гарантирует, что пользователь не получит рекомендацию уже прочитанного контента.

---

## Zero-Shot классификация

Embeddings позволяют классифицировать текст **без обучающих примеров** (zero-shot). Принцип: сравниваем эмбеддинг классифицируемого объекта с эмбеддингами описаний классов и выбираем ближайший.

### Функция поиска ближайшего класса

```python
def find_closest(query_vector, embeddings):
    distances = []
    for i, emb in enumerate(embeddings):
        dist = distance.cosine(query_vector, emb)
        distances.append({'index': i, 'distance': dist})
    return min(distances, key=lambda x: x['distance'])
```

### Простая классификация (по названиям меток)

```python
topics = [
    {'label': 'Tech'},
    {'label': 'Science'},
    {'label': 'Sport'},
    {'label': 'Business'}
]

class_descriptions = [topic['label'] for topic in topics]
class_embeddings = create_embeddings(class_descriptions)

article = {
    'headline': 'How NVIDIA GPUs Could Decide Who Wins the AI Race',
    'keywords': ['ai', 'business', 'computers']
}

def create_article_text(article):
    return f'''Headline: {article['headline']}
Keywords: {', '.join(article['keywords'])}'''

article_text = create_article_text(article)
article_embedding = create_embeddings(article_text)[0]

closest = find_closest(article_embedding, class_embeddings)
label = topics[closest['index']]['label']
print(label)  # → 'Business' (неверно — модель зацепилась за ключевое слово)
```

### Улучшенная классификация (с подробными описаниями классов)

Использование одних только названий меток даёт мало семантического контекста. **Развёрнутые описания** классов значительно улучшают точность классификации:

```python
topics = [
    {'label': 'Tech',     'description': 'A news article about technology'},
    {'label': 'Science',  'description': 'A news article about science'},
    {'label': 'Sport',    'description': 'A news article about sports'},
    {'label': 'Business', 'description': 'A news article about business'}
]

class_descriptions = [topic['description'] for topic in topics]
class_embeddings = create_embeddings(class_descriptions)

article_text = create_article_text(article)
article_embedding = create_embeddings(article_text)[0]

closest = find_closest(article_embedding, class_embeddings)
label = topics[closest['index']]['label']
print(label)  # → 'Tech' (верно!)
```

> **Вывод:** Чем подробнее описание класса, тем лучше модель улавливает его семантику и тем точнее классификация.

---

## Зависимости

```
openai
python-dotenv
scipy
numpy
```

## Связанные темы

- [[OpenAI_API/Working_with_Embeddings]] — основы эмбеддингов, API, косинусное расстояние, t-SNE
- [[Exercises/09_Working_with_Embeddings_Exercise]] — практическое задание по теме
- [[OpenAI_API/Introduction_to_OpenAI_API]] — основы работы с OpenAI API
- [[LLMOps/Development_Phase]] — RAG-архитектура использует embeddings для семантического поиска
