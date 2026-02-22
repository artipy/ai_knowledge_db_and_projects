# Построение Pipeline в Hugging Face

## Обзор

`pipeline` — это высокоуровневый API библиотеки `transformers`, позволяющий быстро запускать модели для решения стандартных NLP-задач. Каждая задача требует своей специализированной модели для достижения наилучшей точности.

Базовое введение в Pipeline: [[Getting_Started_with_Hugging_Face]]

---

## Классификация текста (Text Classification)

Классификация текста позволяет отнести текст к определённой категории. Наиболее распространённая задача — анализ тональности (sentiment analysis). Для каждого вида классификации используется своя обученная модель.

### Анализ тональности

```python
from transformers import pipeline

my_pipeline = pipeline(
    'text-classification',
    model='distilbert-base-uncased-finetuned-sst-2-english'
)

print(my_pipeline('Wi-Fi is slower than a snail today!'))
```

### Проверка грамматической корректности

```python
grammar_checker = pipeline(
    'text-classification',
    model='abdulmatinomotos/English_Grammar_Checker'
)

print(grammar_checker('He eat pizza every day.'))
```

### Question Natural Language Inference (QNLI)

QNLI определяет, является ли переданное утверждение корректным ответом на вопрос. Модели передаётся пара: вопрос и предполагаемый ответ.

```python
classifier = pipeline(
    'text-classification',
    model='cross-encoder/qnli-electra-base'
)

classifier('Where is Seattle located?, Seattle is located in Washington state.')
```

### Zero-Shot классификация

Zero-Shot классификация позволяет назначать категории без предварительного обучения на этих категориях. Категории задаются динамически при вызове.

```python
classifier = pipeline(
    'zero-shot-classification',
    model='facebook/bart-large-mnli'
)

text = 'Hey, Datacamp; we would like to feature your courses in our newsletter!'
categories = ['marketing', 'sales', 'support']

output = classifier(text, categories)

# Получение наиболее подходящей категории
print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")
```

**Когда использовать Zero-Shot:**
- Категории заранее неизвестны или могут меняться
- Нет размеченных данных для дообучения
- Нужна быстрая прототипизация классификатора

---

## Резюмирование текста (Text Summarization)

Резюмирование полезно при работе с длинными отчётами или документами. Существует два основных подхода:

### Экстрактивное резюмирование

Извлекает ключевые предложения из исходного текста без изменений.

```python
summarizer = pipeline(
    'summarization',
    model='nyamuda/extractive-summarization'
)

text = 'This is my really large text about Data Science...'
summary_text = summarizer(text)

print(summary_text[0]['summary_text'])
```

### Абстрактивное резюмирование

Перефразирует текст, добавляя новую информацию и делая его более читабельным.

```python
abstractive_sum = pipeline(
    'summarization',
    model='sshleifer/distilbart-cnn-12-6'
)

text = 'This is my really large text about Data Science...'
summary_text = abstractive_sum(text)

print(summary_text[0]['summary_text'])
```

### Управление длиной резюме

При резюмировании можно управлять длиной ответа:

```python
pipeline(
    'summarization',
    min_new_tokens=50,
    max_new_tokens=250
)
```

| Параметр | Описание |
|---|---|
| `min_new_tokens` | Минимальное количество новых токенов в ответе |
| `max_new_tokens` | Максимальное количество новых токенов в ответе |

---

## Auto-классы и токенизаторы

Auto-классы — это более гибкий способ загрузки моделей и токенизаторов без ручного указания конкретных классов. Они предоставляют больше возможностей по сравнению с `pipeline`, что делает их идеальными для серьёзной разработки.

**Сравнение подходов:**
- `pipeline` — быстрые эксперименты, минимальный код
- Auto-классы — полный контроль над каждым шагом работы модели

### Загрузка модели

Для каждой задачи используется соответствующий класс:

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)
```

### Загрузка токенизатора

Рекомендуется всегда использовать тот токенизатор, который был использован при обучении модели. В `pipeline` токенизатор применяется автоматически.

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)

# Токенизация текста
tokens = tokenizer.tokenize('AI: Helping robots think and humans overthink :)')
print(tokens)
```

> Разные модели по-разному разбивают текст на токены — это важно учитывать при смене модели.

### Связка Auto-классов с Pipeline

Загруженные модель и токенизатор можно передать в `pipeline` для полного контроля над поведением:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

my_model = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)

my_tokenizer = AutoTokenizer.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)

my_pipeline = pipeline(
    'sentiment-analysis',
    model=my_model,
    tokenizer=my_tokenizer
)
```

**Классы для разных задач:**

| Задача | Auto-класс |
|---|---|
| Классификация текста | `AutoModelForSequenceClassification` |
| Распознавание именованных сущностей | `AutoModelForTokenClassification` |
| Ответы на вопросы | `AutoModelForQuestionAnswering` |
| Генерация текста | `AutoModelForCausalLM` |
| Резюмирование | `AutoModelForSeq2SeqLM` |

---

## Ответы на вопросы по документам (Document QA)

Document QA модели позволяют отвечать на вопросы по содержимому документов — например, "Какая была выручка в прошлом году?". Модели передаются два аргумента: документ и вопрос.

### Работа с PDF-файлами

Для чтения PDF используется библиотека `pypdf`:

```bash
pip install pypdf
```

```python
from pypdf import PdfReader
from transformers import pipeline

# Чтение PDF-файла
reader = PdfReader('path_to_file.pdf')

document_text = ''
for page in reader.pages:
    document_text += page.extract_text()

# Подключение модели
qa_pipeline = pipeline(
    task='question-answering',
    model='distilbert-base-cased-distilled-squad'
)

question = 'Your question?'

result = qa_pipeline(question=question, context=document_text)

print(f"Answer is: {result['answer']}")
```

**Поле `context`** — это текст документа, в котором модель ищет ответ. Модель не генерирует ответ из общих знаний, а извлекает его непосредственно из переданного контекста.

---

## Выбор подхода

| Задача | Рекомендуемый подход |
|---|---|
| Быстрый прототип | `pipeline` |
| Кастомизация токенизатора | Auto-классы |
| Контроль над инференсом | Auto-классы + `pipeline` |
| Продакшн-разработка | Auto-классы |

---

## Связанные темы

- [[Getting_Started_with_Hugging_Face]] — введение в Hugging Face, базовый Pipeline и работа с датасетами
- [[Working_with_OpenAI_API_in_Python]] — альтернативный подход к NLP-задачам через OpenAI API
- [[Local_LLM_Deployment/Local_LLM_Deployment_with_LM_Studio]] — локальный запуск моделей без Hugging Face
- [[Prompt_Engineering/Prompt_Engineering_Best_Practices]] — эффективные промпты для NLP-задач
