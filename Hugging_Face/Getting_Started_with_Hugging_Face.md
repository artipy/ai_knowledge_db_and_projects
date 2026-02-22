# Введение в Hugging Face

## Что такое Hugging Face?

Hugging Face — это платформа, где сообщество ИИ-разработчиков может получить доступ к последним современным моделям и наборам данных для обучения.

**Ключевые возможности платформы:**
- Доступ к state-of-the-art моделям машинного обучения
- Библиотеки наборов данных для обучения и дообучения моделей
- Хорошо задокументированные Python-библиотеки
- Возможность использования моделей локально или через провайдеров

## Основные библиотеки Hugging Face

### 1. Transformers

Библиотека `transformers` предназначена для локального использования моделей, размещенных на Hugging Face.

**Установка:**
```bash
pip install transformers
```

**Базовое использование через Pipeline:**

```python
from transformers import pipeline

# Создание pipeline для генерации текста
gpt2_pipeline = pipeline(task="text-generation", model="openai-community/gpt2")

# Генерация текста
print(gpt2_pipeline('What is AI?'))
```

**Pipeline** — это высокоуровневый API, который упрощает использование моделей для различных задач:
- `text-generation` — генерация текста
- `text-classification` — классификация текста
- `sentiment-analysis` — анализ тональности
- `question-answering` — ответы на вопросы
- `translation` — перевод
- и многие другие

### 2. Управление параметрами генерации

Pipeline поддерживает множество параметров для контроля генерации:

```python
results = gpt2_pipeline(
    'What if AI?',
    max_new_tokens=10,        # Максимальное количество новых токенов
    num_return_sequences=2    # Количество вариантов ответа
)

for result in results:
    print(result['generated_text'])
```

**Основные параметры:**
- `max_new_tokens` — ограничение на количество генерируемых токенов
- `num_return_sequences` — количество вариантов генерации
- `temperature` — контроль случайности (не показан в примере, но доступен)
- `top_p`, `top_k` — стратегии сэмплирования

### 3. InferenceClient для удаленного использования

Для использования моделей через провайдера используется `InferenceClient`:

```python
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    api_key=os.getenv('HF_TOKEN'),
    provider='together'  # Провайдер инференса
)

completion = client.chat.completions.create(
    model='model_name',
    messages=[
        {
            'role': 'user',
            'content': 'What if AI?'
        }
    ]
)

print(completion.choices[0].message)
```

**Преимущества удаленного инференса:**
- Не требует локальных вычислительных ресурсов
- Доступ к более мощным моделям
- Быстрый старт без скачивания моделей

## Работа с Hugging Face Datasets

### Установка библиотеки

```bash
pip install datasets
```

### Загрузка наборов данных

Hugging Face предоставляет тысячи готовых наборов данных для различных задач:

```python
from datasets import load_dataset

# Загрузка всего датасета
data = load_dataset('IVN-RIN/BioBERT_Italian')

# Загрузка конкретного split (train, test, validation)
data = load_dataset('IVN-RIN/BioBERT_Italian', split='train')
```

**Каждый набор данных содержит:**
- Карточку с описанием (dataset card)
- Информацию о способе сбора данных
- Язык(и) датасета
- Предназначение и примеры использования
- Разбиение на train/test/validation

### Формат Apache Arrow

Большинство наборов данных Hugging Face хранятся в формате **Apache Arrow** — это колоночное хранилище данных.

**Преимущества колоночного формата:**
- Данные одной колонки хранятся вместе
- Значительно ускоряется поиск и фильтрация
- Эффективное использование памяти
- Быстрые операции над столбцами

### Работа с данными

Управление данными в Apache Arrow немного отличается от pandas:

**Фильтрация данных:**

```python
# Использование метода filter с lambda-функцией
filtered = data.filter(lambda row: " bella " in row['text'])
print(filtered)
```

**Выборка данных:**

```python
# Использование метода select для выбора строк по индексам
sliced = filtered.select(range(2))  # Выбрать первые 2 строки
print(sliced[0]['text'])
```

**Основные методы для работы с datasets:**
- `.filter()` — фильтрация строк по условию
- `.select()` — выбор строк по индексам
- `.map()` — применение функции к каждой строке
- `.shuffle()` — перемешивание данных
- `.train_test_split()` — разбиение на train/test

## Поиск моделей и датасетов

На официальной странице Hugging Face доступно поисковое меню с фильтрами для поиска:
- **Моделей** — по задаче, языку, размеру, лицензии
- **Датасетов** — по языку, задаче, размеру, лицензии

## Связанные темы

- [[Building_Pipelines_with_Hugging_Face]] — углублённое руководство по Pipeline: классификация, резюмирование, Auto-классы, Document QA
- [[Working_with_OpenAI_API_in_Python]] — работа с OpenAI API для сравнения подходов
- [[Local_LLM_Deployment/Local_LLM_Deployment_with_LM_Studio]] — локальный деплой моделей через LM Studio
- [[Python_for_AI/Python_Decorators]] — полезные Python-паттерны для работы с AI

## Дополнительные ресурсы

- Официальная документация: https://huggingface.co/docs
- Hugging Face Hub: https://huggingface.co/models
- Datasets Hub: https://huggingface.co/datasets
- Курсы Hugging Face: https://huggingface.co/learn
