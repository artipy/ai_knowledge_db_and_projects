# Библиотека Tenacity для управления повторными попытками

Библиотека `tenacity` — это мощный инструмент Python для реализации логики повторных попыток (retry logic) при работе с внешними сервисами, API и нестабильными операциями. Для AI engineers эта библиотека является критически важной при работе с API языковых моделей, которые могут возвращать временные ошибки, ограничения по rate limits или случайные сбои сети.

## Связанные заметки

- [[Python_for_AI/Python_Decorators|Декораторы в Python]] - основы декораторов, которые активно используются в tenacity
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - практические примеры работы с API, где критична обработка ошибок
- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - базовая информация о подключению к API
- [[Local_LLM_Deployment/Local_LLM_Deployment_with_LM_Studio|Развертывание локальных LLM с LM Studio]] - работа с локальными моделями, где также важна устойчивость к ошибкам

## Зачем AI Engineer нужна библиотека Tenacity?

При работе с AI API вы неизбежно столкнетесь с различными проблемами:

### 1. **Rate Limiting (Ограничение скорости запросов)**
API провайдеры (OpenAI, Anthropic, Google) устанавливают лимиты на количество запросов в минуту (RPM) и токенов в минуту (TPM). При превышении лимитов API возвращает ошибку `429 Too Many Requests`.

### 2. **Временные сбои сети**
Сетевые проблемы, таймауты соединения или временная недоступность серверов могут привести к ошибкам `ConnectionError`, `Timeout`, `503 Service Unavailable`.

### 3. **Внутренние ошибки сервера**
API может вернуть ошибку `500 Internal Server Error` или `502 Bad Gateway` из-за временных проблем на стороне провайдера.

### 4. **Перегрузка серверов**
В пиковые часы серверы могут быть перегружены, что приводит к ошибкам `503` или увеличению времени ответа.

### 5. **Стоимость запросов**
Каждый запрос к API стоит денег. Без правильной retry-логики вы можете потерять средства на неудачных запросах, которые можно было бы успешно повторить.

**Библиотека tenacity решает все эти проблемы**, предоставляя гибкую и декларативную систему для автоматических повторных попыток с настраиваемыми стратегиями ожидания, условиями остановки и обработкой исключений.

## Установка

```bash
pip install tenacity
```

## Основные концепции

### 1. Базовый retry с декоратором

Самый простой способ использования — декоратор `@retry`:

```python
from tenacity import retry
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry
def call_openai_api(prompt):
    """Функция с автоматическими повторными попытками"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# При возникновении любой ошибки функция автоматически повторит запрос
result = call_openai_api("Расскажи о машинном обучении")
```

**По умолчанию**: бесконечные повторы без задержки между попытками (не рекомендуется для production).

### 2. Ограничение количества попыток

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def call_api_with_limit(prompt):
    """Максимум 3 попытки"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### 3. Экспоненциальная задержка (Exponential Backoff)

Экспоненциальная задержка — это стратегия, где время ожидания между попытками экспоненциально увеличивается: 1с, 2с, 4с, 8с и т.д.

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=60)
)
def call_api_with_backoff(prompt):
    """
    Повторные попытки с экспоненциальной задержкой:
    - 1 попытка: сразу
    - 2 попытка: через 1 секунду
    - 3 попытка: через 2 секунды
    - 4 попытка: через 4 секунды
    - 5 попытка: через 8 секунд
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

**Параметры**:
- `multiplier` — множитель для экспоненты (обычно 1)
- `min` — минимальное время ожидания в секундах
- `max` — максимальное время ожидания в секундах

## Практические паттерны для AI Engineers

### Паттерн 1: Обработка Rate Limits (429 ошибка)

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import RateLimitError, APIError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=120),
    before_sleep=lambda retry_state: logger.info(
        f"Rate limit exceeded. Retry #{retry_state.attempt_number} after {retry_state.next_action.sleep} seconds"
    )
)
def call_api_with_rate_limit_handling(prompt):
    """
    Обработка rate limits с умной стратегией повторов:
    - Повторяем только при RateLimitError и APIError
    - Экспоненциальная задержка: 4с, 8с, 16с, 32с, 64с
    - Логируем каждую попытку
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Использование
try:
    result = call_api_with_rate_limit_handling("Объясни квантовые вычисления")
    print(result)
except RateLimitError:
    print("Превышен лимит запросов после всех попыток")
```

### Паттерн 2: Батчевая обработка с retry

При обработке больших объемов данных важно обрабатывать каждый элемент с retry-логикой:

```python
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(Exception)
)
def process_single_item(item: str) -> str:
    """Обработка одного элемента с повторными попытками"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Резюмируй: {item}"}],
        max_tokens=100
    )
    return response.choices[0].message.content

def process_batch(items: List[str]) -> List[dict]:
    """
    Обработка батча с отслеживанием успешных и неудачных элементов
    """
    results = []

    for idx, item in enumerate(items):
        try:
            summary = process_single_item(item)
            results.append({
                "index": idx,
                "item": item,
                "summary": summary,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "index": idx,
                "item": item,
                "error": str(e),
                "status": "failed"
            })
            logger.error(f"Failed to process item {idx} after retries: {e}")

    return results

# Использование
texts = [
    "Длинный текст о машинном обучении...",
    "Длинный текст об искусственном интеллекте...",
    "Длинный текст о нейронных сетях..."
]

results = process_batch(texts)

# Статистика
successful = sum(1 for r in results if r["status"] == "success")
failed = sum(1 for r in results if r["status"] == "failed")

print(f"Успешно обработано: {successful}/{len(texts)}")
print(f"Ошибок: {failed}/{len(texts)}")
```

### Паттерн 3: Retry с таймаутом

```python
from tenacity import retry, stop_after_delay, wait_exponential
import time

@retry(
    stop=stop_after_delay(60),  # Остановить через 60 секунд
    wait=wait_exponential(multiplier=1, max=10)
)
def call_api_with_timeout(prompt: str) -> str:
    """
    Повторяем попытки максимум 60 секунд
    После этого выбрасывается RetryError
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        timeout=30  # Таймаут самого запроса
    )
    return response.choices[0].message.content
```

### Паттерн 4: Комбинированные условия остановки

```python
from tenacity import retry, stop_after_attempt, stop_after_delay

@retry(
    stop=(stop_after_attempt(5) | stop_after_delay(120))  # Максимум 5 попыток ИЛИ 120 секунд
)
def call_api_combined_stop(prompt: str) -> str:
    """
    Останавливаемся при достижении любого из условий:
    - 5 попыток
    - 120 секунд общего времени
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Паттерн 5: Условные повторы (Retry only on specific errors)

```python
from tenacity import retry, retry_if_exception_type, retry_if_not_exception_type
from openai import APIError, AuthenticationError, RateLimitError

@retry(
    retry=(
        retry_if_exception_type((RateLimitError, APIError)) &
        retry_if_not_exception_type(AuthenticationError)
    ),
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=4, max=60)
)
def call_api_selective_retry(prompt: str) -> str:
    """
    Повторяем только при RateLimitError и APIError
    НЕ повторяем при AuthenticationError (невалидный API ключ)
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Паттерн 6: Кастомные callback-функции

```python
from tenacity import retry, before_log, after_log
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_before_retry(retry_state):
    """Функция вызывается перед каждой попыткой"""
    logger.info(
        f"Попытка #{retry_state.attempt_number} | "
        f"Функция: {retry_state.fn.__name__}"
    )

def log_after_retry(retry_state):
    """Функция вызывается после каждой попытки"""
    if retry_state.outcome.failed:
        logger.error(
            f"Попытка #{retry_state.attempt_number} провалилась: "
            f"{retry_state.outcome.exception()}"
        )

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    before=log_before_retry,
    after=log_after_retry
)
def call_api_with_logging(prompt: str) -> str:
    """Функция с детальным логированием каждой попытки"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## Продвинутые техники

### Retry с fallback на другую модель

```python
from tenacity import retry, RetryError

@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
def call_gpt4(prompt: str) -> str:
    """Попытка использовать GPT-4"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_with_fallback(prompt: str) -> dict:
    """
    Сначала пытаемся использовать GPT-4
    При неудаче переключаемся на GPT-3.5-turbo
    """
    try:
        result = call_gpt4(prompt)
        return {
            "content": result,
            "model": "gpt-4",
            "fallback_used": False
        }
    except RetryError:
        logger.warning("GPT-4 недоступен, используем fallback на GPT-3.5")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "content": response.choices[0].message.content,
            "model": "gpt-3.5-turbo",
            "fallback_used": True
        }

# Использование
result = call_with_fallback("Объясни теорию относительности")
print(f"Модель: {result['model']}")
print(f"Fallback использован: {result['fallback_used']}")
print(f"Результат: {result['content']}")
```

### Асинхронный retry для concurrent запросов

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import AsyncOpenAI
import asyncio

async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30)
)
async def async_call_api(prompt: str) -> str:
    """Асинхронный вызов API с retry логикой"""
    response = await async_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def process_multiple_prompts(prompts: List[str]) -> List[str]:
    """Параллельная обработка нескольких промптов"""
    tasks = [async_call_api(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Обработка результатов
    processed_results = []
    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Prompt {idx} failed: {result}")
            processed_results.append(None)
        else:
            processed_results.append(result)

    return processed_results

# Использование
prompts = [
    "Что такое искусственный интеллект?",
    "Что такое машинное обучение?",
    "Что такое глубокое обучение?"
]

results = asyncio.run(process_multiple_prompts(prompts))
```

### Retry с сохранением истории попыток

```python
from tenacity import Retrying, stop_after_attempt, wait_fixed
from datetime import datetime

def call_api_with_history(prompt: str) -> dict:
    """
    Вызов API с сохранением истории всех попыток
    """
    history = []

    for attempt in Retrying(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2)
    ):
        with attempt:
            start_time = datetime.now()
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                duration = (datetime.now() - start_time).total_seconds()

                history.append({
                    "attempt": attempt.retry_state.attempt_number,
                    "success": True,
                    "duration": duration,
                    "timestamp": start_time.isoformat()
                })

                return {
                    "content": response.choices[0].message.content,
                    "attempts": attempt.retry_state.attempt_number,
                    "history": history
                }
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                history.append({
                    "attempt": attempt.retry_state.attempt_number,
                    "success": False,
                    "error": str(e),
                    "duration": duration,
                    "timestamp": start_time.isoformat()
                })
                raise

# Использование
result = call_api_with_history("Расскажи о Python")
print(f"Успешно выполнено за {result['attempts']} попыток")
print(f"История: {result['history']}")
```

## Мониторинг и метрики

### Класс для сбора статистики retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class RetryMetrics:
    """Класс для сбора метрик retry-операций"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_retries: int = 0
    total_duration: float = 0.0
    errors: List[str] = field(default_factory=list)

    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return (self.successful_calls / self.total_calls) * 100

    def avg_duration(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.total_duration / self.total_calls

    def avg_retries_per_call(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.total_retries / self.total_calls

    def report(self) -> str:
        return f"""
=== Retry Metrics Report ===
Total API calls: {self.total_calls}
Successful: {self.successful_calls}
Failed: {self.failed_calls}
Success rate: {self.success_rate():.2f}%
Total retries: {self.total_retries}
Avg retries per call: {self.avg_retries_per_call():.2f}
Avg duration: {self.avg_duration():.2f}s
Most common errors: {self._top_errors()}
        """

    def _top_errors(self, n=3) -> str:
        if not self.errors:
            return "None"
        from collections import Counter
        common = Counter(self.errors).most_common(n)
        return ", ".join([f"{err}: {count}" for err, count in common])

# Глобальный объект метрик
metrics = RetryMetrics()

def track_metrics(retry_state):
    """Callback для отслеживания метрик"""
    metrics.total_retries += retry_state.attempt_number - 1
    if retry_state.outcome.failed:
        error_type = type(retry_state.outcome.exception()).__name__
        metrics.errors.append(error_type)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=10),
    after=track_metrics
)
def monitored_api_call(prompt: str) -> str:
    """API вызов с мониторингом метрик"""
    start = time.time()
    metrics.total_calls += 1

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        metrics.successful_calls += 1
        metrics.total_duration += time.time() - start
        return response.choices[0].message.content
    except Exception as e:
        metrics.failed_calls += 1
        metrics.total_duration += time.time() - start
        raise

# Использование
prompts = ["Что такое Python?", "Что такое AI?", "Что такое ML?"]

for prompt in prompts:
    try:
        result = monitored_api_call(prompt)
    except Exception:
        pass

# Вывод отчета
print(metrics.report())
```

## Best Practices для AI Engineers

### 1. **Всегда используйте экспоненциальную задержку**
Не используйте фиксированные задержки для API запросов. Экспоненциальная задержка снижает нагрузку на сервер и увеличивает вероятность успешного запроса.

```python
# ✅ ХОРОШО
wait=wait_exponential(multiplier=1, min=4, max=60)

# ❌ ПЛОХО
wait=wait_fixed(1)  # Может усугубить проблему rate limiting
```

### 2. **Не повторяйте невосстановимые ошибки**
Некоторые ошибки не имеет смысла повторять (например, `AuthenticationError`, `InvalidRequestError`):

```python
from openai import AuthenticationError, InvalidRequestError

@retry(
    retry=retry_if_not_exception_type((AuthenticationError, InvalidRequestError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=4, max=60)
)
def smart_retry(prompt: str):
    # Не будет повторять при проблемах с аутентификацией
    pass
```

### 3. **Логируйте все попытки**
Для production систем критически важно знать, сколько раз происходили повторы:

```python
@retry(
    stop=stop_after_attempt(3),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry #{retry_state.attempt_number} after error: {retry_state.outcome.exception()}"
    )
)
def logged_call(prompt: str):
    pass
```

### 4. **Устанавливайте разумные лимиты**
Не делайте бесконечные повторы. Установите максимальное количество попыток И максимальное время:

```python
@retry(
    stop=(stop_after_attempt(5) | stop_after_delay(300)),  # Максимум 5 попыток или 5 минут
    wait=wait_exponential(multiplier=2, max=60)
)
def safe_retry(prompt: str):
    pass
```

### 5. **Используйте fallback стратегии**
При критических операциях имейте запасной план:

```python
def critical_operation(data):
    try:
        return call_gpt4(data)
    except RetryError:
        # Fallback на более дешевую модель
        return call_gpt35(data)
```

### 6. **Мониторьте метрики retry**
Собирайте статистику по повторным попыткам для оптимизации:
- Процент успешных запросов после retry
- Среднее количество попыток на запрос
- Самые частые типы ошибок
- Общее время, потраченное на retry

### 7. **Используйте асинхронность для batch операций**
При обработке множества запросов используйте асинхронные версии с retry:

```python
@retry(stop=stop_after_attempt(3))
async def async_call(prompt):
    return await async_client.chat.completions.create(...)

# Обработка 100 запросов параллельно
results = await asyncio.gather(*[async_call(p) for p in prompts])
```

## Сравнение стратегий ожидания

| Стратегия | Формула | Когда использовать | Пример задержек |
|-----------|---------|-------------------|-----------------|
| `wait_fixed(n)` | Всегда `n` секунд | Редко (только для тестов) | 2с, 2с, 2с, 2с |
| `wait_random(min, max)` | Случайно между `min` и `max` | Распределение нагрузки | 1.3с, 4.7с, 2.1с |
| `wait_exponential(multiplier, min, max)` | `multiplier * 2^(attempt-1)` | **Рекомендуется для API** | 1с, 2с, 4с, 8с |
| `wait_exponential_jitter()` | Экспонента + случайность | Избежание "thundering herd" | 1.2с, 2.7с, 4.3с |
| `wait_chain(*waits)` | Комбинация стратегий | Сложные сценарии | 1с, 2с, затем random |

## Реальный пример: Production-ready обертка для OpenAI

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type,
    before_sleep_log
)
from openai import OpenAI, RateLimitError, APIError, Timeout
from typing import Optional, List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResilientOpenAIClient:
    """
    Production-ready обертка для OpenAI с встроенной retry-логикой
    """

    def __init__(self, api_key: str, default_model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.default_model = default_model
        self.metrics = RetryMetrics()

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIError, Timeout)),
        stop=stop_after_attempt(5),
        wait=wait_exponential_jitter(initial=2, max=120, jitter=5),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Устойчивый вызов chat completion API

        Args:
            messages: Список сообщений в формате [{"role": "...", "content": "..."}]
            model: Название модели (по умолчанию используется self.default_model)
            temperature: Температура генерации (0-2)
            max_tokens: Максимальное количество токенов в ответе
            **kwargs: Дополнительные параметры для API

        Returns:
            Текст ответа от модели
        """
        self.metrics.total_calls += 1
        start = time.time()

        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            self.metrics.successful_calls += 1
            self.metrics.total_duration += time.time() - start

            return response.choices[0].message.content

        except Exception as e:
            self.metrics.failed_calls += 1
            self.metrics.total_duration += time.time() - start
            self.metrics.errors.append(type(e).__name__)
            logger.error(f"API call failed: {e}")
            raise

    def simple_completion(self, prompt: str, **kwargs) -> str:
        """Упрощенный метод для single-turn запросов"""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, **kwargs)

    def get_metrics_report(self) -> str:
        """Получить отчет по метрикам"""
        return self.metrics.report()

# Использование
client = ResilientOpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_model="gpt-4"
)

# Простой запрос
response = client.simple_completion("Что такое machine learning?")
print(response)

# Многоэтапный диалог
messages = [
    {"role": "system", "content": "Ты эксперт по Python"},
    {"role": "user", "content": "Объясни list comprehension"}
]
response = client.chat_completion(messages, temperature=0.3)
print(response)

# Получить метрики
print(client.get_metrics_report())
```

## Заключение

Библиотека `tenacity` — это критически важный инструмент для любого AI Engineer, работающего с внешними API. Она позволяет:

✅ **Повысить надежность** — автоматически обрабатывать временные сбои
✅ **Снизить затраты** — не терять деньги на неудачных запросах
✅ **Улучшить UX** — пользователи не видят временные ошибки
✅ **Масштабировать приложения** — корректно обрабатывать rate limits
✅ **Отлаживать проблемы** — детальное логирование всех попыток
✅ **Мониторить систему** — собирать метрики по надежности API

**Главное правило**: Всегда используйте retry-логику при работе с внешними AI API в production-окружении.

## Дополнительные ресурсы

- [Официальная документация Tenacity](https://tenacity.readthedocs.io/)
- [OpenAI Error Handling Guide](https://platform.openai.com/docs/guides/error-codes)
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] — базовые примеры работы с API

---

*Эта заметка создана для AI Engineers, работающих с языковыми моделями и внешними API.*
