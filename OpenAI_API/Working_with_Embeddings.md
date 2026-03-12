# Работа с Embeddings

Embeddings (векторные представления) — это фундаментальное понятие в области обработки естественного языка (NLP), где текст (слова, фразы или целые документы) представляется в числовом виде.

## Что такое Embeddings

Модели embedding отображают текст в **многомерное векторное пространство**. Числа, выдаваемые моделью, описывают положение текста в этом пространстве. Семантически похожие фрагменты текста — например, «учитель» и «ученик» — располагаются ближе друг к другу, а непохожие — дальше.

Эта способность улавливать семантическую близость позволяет моделям понимать **полный контекст и смысл** слова. Например, фразы «Как пройти к супермаркету?» и «Можно ли мне узнать, как пройти к магазину?» семантически очень похожи, несмотря на минимальное количество общих слов.

## Основные применения

- **Семантический поиск** — в отличие от keyword-поиска, ищет по смыслу, а не по точному совпадению слов. Запрос преобразуется в вектор и сравнивается с векторами документов
- **Системы рекомендаций** — подбор похожего контента на основе семантического сходства (например, вакансий с похожими описаниями)
- **Классификация** — категоризация текстов по семантическому сходству с эталонными примерами (классификация настроений, кластеризация, тематическая рубрикация)

## Получение Embeddings через API

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input='Embeddings are a numerical representation of text'
)

response_dict = response.model_dump()
embedding = response_dict['data'][0]['embedding']
print(len(embedding))  # 1536 чисел для моделей OpenAI
```

Модели OpenAI возвращают **1536 чисел** для любого входного текста, независимо от его длины.

### Пакетная обработка

Передача нескольких текстов за один запрос значительно эффективнее отдельных вызовов:

```python
articles = [
    {"headline": "Economic Growth Continues Amid Global Uncertainty", "topic": "Business"},
    {"headline": "Scientists Make Breakthrough Discovery in Renewable Energy", "topic": "Science"},
    {"headline": "Tech Company Launches Innovative Product", "topic": "Tech"},
    # ...
]

headline_text = [article['headline'] for article in articles]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=headline_text  # список строк
)

response_dict = response.model_dump()

for i, article in enumerate(articles):
    article['embedding'] = response_dict['data'][i]['embedding']
```

### Вспомогательная функция

```python
def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]

# Список эмбеддингов для нескольких текстов
embeddings = create_embeddings(['Python is the best!', 'R is the best!'])

# Один эмбеддинг — обращаемся по индексу 0
single_embedding = create_embeddings('Python is the best!')[0]
```

## Визуализация векторного пространства

Для визуализации используется снижение размерности с помощью **t-SNE** (t-distributed Stochastic Neighbor Embedding) — метод из `scikit-learn`, сокращающий 1536 измерений до 2:

```python
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

embeddings = [article['embedding'] for article in articles]

# perplexity должна быть меньше числа точек данных
tsne = TSNE(n_components=2, perplexity=5)
embeddings_2d = tsne.fit_transform(np.array(embeddings))

plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

topics = [article['topic'] for article in articles]
for i, topic in enumerate(topics):
    plt.annotate(topic, (embeddings_2d[i, 0], embeddings_2d[i, 1]))

plt.show()
```

> **Важно:** t-SNE полезен для визуализации, но приводит к потере информации. Используйте его только для исследования данных, не для вычислений.

Результат: заголовки с одинаковыми темами (Sport, Business, Tech, Science) сгруппируются в отдельные кластеры — модель уловила их семантическое сходство.

## Вычисление семантического сходства

Для измерения сходства между векторами используется **косинусное расстояние** из `scipy.spatial`. Значение варьируется от 0 (максимальное сходство) до 2 (полная противоположность):

```python
from scipy.spatial import distance

# Простой пример: два вектора в 2D
distance.cosine([0, 1], [1, 0])  # → 1.0
```

### Семантический поиск по заголовкам

```python
from scipy.spatial import distance
import numpy as np

search_text = 'computer'
search_embedding = create_embeddings(search_text)[0]

distances = []
for article in articles:
    dist = distance.cosine(search_embedding, article['embedding'])
    distances.append(dist)

# Статья с минимальным расстоянием — наиболее похожая
min_dist_ind = np.argmin(distances)
print(articles[min_dist_ind]['headline'])
# → 'Tech Company Launches Innovative Product to Improve Online Accessibility'
```

## Зависимости

```
openai
python-dotenv
scipy
scikit-learn
numpy
matplotlib
```

## Связанные темы

- [[Exercises/09_Working_with_Embeddings_Exercise]] — практическое задание по теме
- [[OpenAI_API/Introduction_to_OpenAI_API]] — основы работы с OpenAI API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python]] — Python-интеграция и паттерны
- [[LLMOps/Development_Phase]] — RAG-архитектура использует embeddings для поиска в базе знаний
- [[Hugging_Face/Building_Pipelines_with_Hugging_Face]] — альтернативные модели через `sentence-transformers`
