# Декораторы в Python

Декораторы — это мощный инструмент Python, позволяющий изменять или расширять поведение функций и методов без изменения их исходного кода. Для AI engineers декораторы являются незаменимым инструментом для добавления функциональности к API вызовам, логирования, кеширования, измерения производительности и обработки ошибок.

## Связанные заметки

- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]] - практическое применение декораторов для обработки ошибок API
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]] - примеры использования API, где декораторы улучшают надёжность
- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]] - базовые концепции работы с API
- [[Prompt_Engineering/Prompt_Engineering_for_Business_Applications|Prompt Engineering для бизнес-приложений]] - практическое применение API для бизнес-задач, где важна надежная обработка ошибок

## Что такое декоратор?

**Декоратор** — это функция, которая принимает другую функцию в качестве аргумента и возвращает новую функцию с расширенным или изменённым поведением. Декораторы используют концепцию **функций высшего порядка** (higher-order functions) и **замыканий** (closures).

### Базовый синтаксис

```python
@decorator
def function():
    pass
```

Это эквивалентно:

```python
def function():
    pass

function = decorator(function)
```

## Зачем AI Engineer нужны декораторы?

При работе с AI/ML системами декораторы решают множество типичных задач:

### 1. **Обработка ошибок и повторные попытки**
API языковых моделей могут возвращать ошибки — декораторы автоматизируют retry-логику.

### 2. **Кеширование результатов**
Запросы к LLM стоят денег и времени — кеширование одинаковых запросов экономит ресурсы.

### 3. **Логирование и мониторинг**
Отслеживание всех вызовов API, параметров и результатов критично для отладки и аудита.

### 4. **Измерение производительности**
Понимание, сколько времени занимает каждый запрос к модели, помогает оптимизировать систему.

### 5. **Контроль доступа и валидация**
Проверка прав доступа, валидация входных данных перед отправкой в модель.

### 6. **Rate limiting**
Ограничение частоты запросов к API для соблюдения лимитов провайдера.

## Основы декораторов

### Пример 1: Простейший декоратор

```python
def simple_decorator(func):
    """Простейший декоратор, который оборачивает функцию"""
    def wrapper():
        print("До вызова функции")
        func()
        print("После вызова функции")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

# Использование
say_hello()
```

**Вывод:**
```
До вызова функции
Hello!
После вызова функции
```

### Пример 2: Декоратор с аргументами функции

```python
def decorator_with_args(func):
    """Декоратор, который работает с функциями, принимающими аргументы"""
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула: {result}")
        return result
    return wrapper

@decorator_with_args
def add(a, b):
    return a + b

# Использование
result = add(3, 5)
print(f"Итоговый результат: {result}")
```

**Вывод:**
```
Вызов функции add с аргументами: (3, 5), {}
Функция add вернула: 8
Итоговый результат: 8
```

### Пример 3: Сохранение метаданных функции

```python
from functools import wraps

def proper_decorator(func):
    """Правильный декоратор с сохранением метаданных"""
    @wraps(func)  # Сохраняет __name__, __doc__ и другие атрибуты
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@proper_decorator
def important_function():
    """Эта функция делает что-то важное"""
    pass

# Без @wraps имя функции было бы "wrapper"
print(important_function.__name__)  # important_function
print(important_function.__doc__)   # Эта функция делает что-то важное
```

**Важно:** Всегда используйте `@wraps(func)` внутри декоратора для сохранения метаданных исходной функции.

## Практические декораторы для AI Engineers

### Декоратор 1: Логирование API вызовов

```python
import logging
from functools import wraps
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_api_call(func):
    """Логирует все вызовы API с параметрами и результатами"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Логируем входные параметры
        logger.info(f"[{datetime.now()}] Calling {func.__name__}")
        logger.info(f"Arguments: args={args}, kwargs={kwargs}")

        try:
            # Выполняем функцию
            result = func(*args, **kwargs)

            # Логируем успешный результат
            logger.info(f"[{datetime.now()}] {func.__name__} completed successfully")
            logger.info(f"Result length: {len(str(result))} characters")

            return result
        except Exception as e:
            # Логируем ошибку
            logger.error(f"[{datetime.now()}] {func.__name__} failed with error: {e}")
            raise

    return wrapper

# Использование
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@log_api_call
def call_openai(prompt: str) -> str:
    """Вызов OpenAI API с логированием"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# При вызове автоматически логируются все детали
result = call_openai("Что такое машинное обучение?")
```

### Декоратор 2: Измерение времени выполнения

```python
import time
from functools import wraps

def measure_time(func):
    """Измеряет время выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        print(f"⏱️ {func.__name__} выполнилась за {duration:.2f} секунд")

        return result
    return wrapper

@measure_time
def slow_api_call(prompt: str) -> str:
    """API вызов с измерением времени"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Использование
result = slow_api_call("Объясни квантовую физику")
# Вывод: ⏱️ slow_api_call выполнилась за 3.42 секунд
```

### Декоратор 3: Кеширование результатов

```python
from functools import wraps
import hashlib
import json

def cache_results(func):
    """Кеширует результаты API вызовов для экономии средств"""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Создаём уникальный ключ на основе аргументов
        cache_key = hashlib.md5(
            json.dumps((args, kwargs), sort_keys=True).encode()
        ).hexdigest()

        # Проверяем наличие в кеше
        if cache_key in cache:
            print(f"✅ Результат из кеша для {func.__name__}")
            return cache[cache_key]

        # Выполняем функцию и кешируем результат
        print(f"🔄 Выполняем {func.__name__} и кешируем результат")
        result = func(*args, **kwargs)
        cache[cache_key] = result

        return result

    # Добавляем метод для очистки кеша
    wrapper.clear_cache = lambda: cache.clear()
    wrapper.cache_info = lambda: f"Размер кеша: {len(cache)} записей"

    return wrapper

@cache_results
def expensive_api_call(prompt: str) -> str:
    """API вызов с кешированием"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Использование
result1 = expensive_api_call("Что такое Python?")  # Вызов API
result2 = expensive_api_call("Что такое Python?")  # Из кеша
result3 = expensive_api_call("Что такое Java?")    # Вызов API

print(expensive_api_call.cache_info())  # Размер кеша: 2 записей
expensive_api_call.clear_cache()  # Очистка кеша
```

### Декоратор 4: Валидация входных данных

```python
from functools import wraps
from typing import get_type_hints

def validate_types(func):
    """Проверяет типы аргументов перед вызовом функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов
        hints = get_type_hints(func)

        # Проверяем позиционные аргументы
        all_args = list(args)
        arg_names = list(hints.keys())[:len(args)]

        for arg_name, arg_value in zip(arg_names, all_args):
            if arg_name in hints:
                expected_type = hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                        f"получен {type(arg_value).__name__}"
                    )

        # Проверяем именованные аргументы
        for arg_name, arg_value in kwargs.items():
            if arg_name in hints:
                expected_type = hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                        f"получен {type(arg_value).__name__}"
                    )

        return func(*args, **kwargs)

    return wrapper

@validate_types
def process_text(text: str, max_length: int = 100) -> str:
    """Обрабатывает текст с валидацией типов"""
    return text[:max_length]

# Использование
result = process_text("Hello, world!", max_length=5)  # ✅ Работает
# result = process_text(123, max_length=5)  # ❌ TypeError
# result = process_text("Hello", max_length="5")  # ❌ TypeError
```

### Декоратор 5: Rate Limiting

```python
import time
from functools import wraps
from collections import deque

def rate_limit(max_calls: int, time_window: int):
    """
    Ограничивает количество вызовов функции

    Args:
        max_calls: Максимальное количество вызовов
        time_window: Временное окно в секундах
    """
    def decorator(func):
        calls = deque()

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # Удаляем старые вызовы за пределами временного окна
            while calls and calls[0] < now - time_window:
                calls.popleft()

            # Проверяем лимит
            if len(calls) >= max_calls:
                sleep_time = time_window - (now - calls[0])
                print(f"⏳ Rate limit достигнут. Ожидание {sleep_time:.2f} секунд...")
                time.sleep(sleep_time)
                calls.popleft()

            # Записываем текущий вызов
            calls.append(time.time())

            return func(*args, **kwargs)

        return wrapper
    return decorator

# Использование: максимум 3 вызова в минуту
@rate_limit(max_calls=3, time_window=60)
def call_limited_api(prompt: str) -> str:
    """API с ограничением 3 запроса в минуту"""
    print(f"🔄 Вызов API: {prompt}")
    # Здесь был бы реальный API вызов
    return f"Ответ на: {prompt}"

# Первые 3 вызова выполнятся сразу, 4-й будет ждать
for i in range(5):
    result = call_limited_api(f"Запрос #{i+1}")
```

### Декоратор 6: Повторные попытки (Simplified Retry)

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Повторяет выполнение функции при ошибке

    Args:
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками
        backoff: Множитель для экспоненциальной задержки
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"❌ Все {max_attempts} попыток исчерпаны")
                        raise

                    print(f"⚠️ Попытка {attempt} не удалась: {e}")
                    print(f"⏳ Повтор через {current_delay:.1f} секунд...")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

@retry(max_attempts=3, delay=1.0, backoff=2.0)
def unstable_api_call(prompt: str) -> str:
    """API вызов, который может падать"""
    import random
    if random.random() < 0.7:  # 70% вероятность ошибки
        raise ConnectionError("API временно недоступен")
    return "Успешный ответ"

# Использование
result = unstable_api_call("Test prompt")
```

## Декораторы с параметрами

### Пример: Параметризованный декоратор логирования

```python
from functools import wraps
import logging

def log_with_level(level: str = "INFO"):
    """
    Декоратор с параметром - уровень логирования

    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            log_func = getattr(logger, level.lower())

            log_func(f"Вызов {func.__name__} с args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            log_func(f"{func.__name__} завершена, результат: {result}")

            return result
        return wrapper
    return decorator

# Использование с разными уровнями логирования
@log_with_level("DEBUG")
def debug_function(x: int) -> int:
    return x * 2

@log_with_level("ERROR")
def critical_function(x: int) -> int:
    return x * 3
```

## Комбинирование декораторов

Декораторы можно комбинировать, применяя несколько к одной функции:

```python
@log_api_call
@measure_time
@cache_results
@retry(max_attempts=3)
def complex_api_call(prompt: str) -> str:
    """
    Функция с множественными декораторами:
    1. Повторные попытки при ошибках
    2. Кеширование результатов
    3. Измерение времени
    4. Логирование вызовов
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

**Важно:** Порядок декораторов имеет значение! Декораторы применяются снизу вверх:
1. Сначала применяется `@retry`
2. Затем `@cache_results`
3. Затем `@measure_time`
4. Последним `@log_api_call`

## Классовые декораторы

Декораторы также можно реализовать как классы:

```python
class CountCalls:
    """Декоратор-класс для подсчёта вызовов функции"""

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Вызов #{self.count} функции {self.func.__name__}")
        return self.func(*args, **kwargs)

    def reset_count(self):
        """Сброс счётчика"""
        self.count = 0

@CountCalls
def api_call(prompt: str) -> str:
    return f"Обработан: {prompt}"

# Использование
api_call("Запрос 1")  # Вызов #1 функции api_call
api_call("Запрос 2")  # Вызов #2 функции api_call
print(f"Всего вызовов: {api_call.count}")  # Всего вызовов: 2
api_call.reset_count()
```

## Продвинутый пример: Production-Ready декоратор для AI API

```python
from functools import wraps
import time
import logging
from typing import Optional, Callable, Any
from dataclasses import dataclass
import hashlib
import json

@dataclass
class APICallMetrics:
    """Метрики вызова API"""
    function_name: str
    duration: float
    success: bool
    cached: bool
    attempt: int
    error: Optional[str] = None

class AIAPIDecorator:
    """
    Production-ready декоратор для AI API с полным набором функций:
    - Retry логика
    - Кеширование
    - Метрики
    - Логирование
    """

    def __init__(
        self,
        max_retries: int = 3,
        cache_enabled: bool = True,
        log_enabled: bool = True,
        metrics_callback: Optional[Callable[[APICallMetrics], None]] = None
    ):
        self.max_retries = max_retries
        self.cache_enabled = cache_enabled
        self.log_enabled = log_enabled
        self.metrics_callback = metrics_callback
        self.cache = {}
        self.logger = logging.getLogger(__name__)

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Проверяем кеш
            if self.cache_enabled:
                cache_key = self._get_cache_key(args, kwargs)
                if cache_key in self.cache:
                    if self.log_enabled:
                        self.logger.info(f"✅ Cache hit for {func.__name__}")

                    metrics = APICallMetrics(
                        function_name=func.__name__,
                        duration=0.0,
                        success=True,
                        cached=True,
                        attempt=0
                    )
                    if self.metrics_callback:
                        self.metrics_callback(metrics)

                    return self.cache[cache_key]

            # Retry логика
            last_exception = None
            for attempt in range(1, self.max_retries + 1):
                start_time = time.time()

                try:
                    if self.log_enabled:
                        self.logger.info(f"🔄 Calling {func.__name__} (attempt {attempt}/{self.max_retries})")

                    result = func(*args, **kwargs)
                    duration = time.time() - start_time

                    # Сохраняем в кеш
                    if self.cache_enabled:
                        cache_key = self._get_cache_key(args, kwargs)
                        self.cache[cache_key] = result

                    # Метрики успеха
                    metrics = APICallMetrics(
                        function_name=func.__name__,
                        duration=duration,
                        success=True,
                        cached=False,
                        attempt=attempt
                    )
                    if self.metrics_callback:
                        self.metrics_callback(metrics)

                    if self.log_enabled:
                        self.logger.info(f"✅ {func.__name__} completed in {duration:.2f}s")

                    return result

                except Exception as e:
                    duration = time.time() - start_time
                    last_exception = e

                    if self.log_enabled:
                        self.logger.warning(f"⚠️ Attempt {attempt} failed: {e}")

                    if attempt < self.max_retries:
                        sleep_time = 2 ** attempt  # Экспоненциальная задержка
                        time.sleep(sleep_time)

            # Все попытки исчерпаны
            metrics = APICallMetrics(
                function_name=func.__name__,
                duration=duration,
                success=False,
                cached=False,
                attempt=self.max_retries,
                error=str(last_exception)
            )
            if self.metrics_callback:
                self.metrics_callback(metrics)

            raise last_exception

        # Добавляем методы управления
        wrapper.clear_cache = lambda: self.cache.clear()
        wrapper.cache_size = lambda: len(self.cache)

        return wrapper

    def _get_cache_key(self, args: tuple, kwargs: dict) -> str:
        """Генерирует ключ кеша на основе аргументов"""
        return hashlib.md5(
            json.dumps((args, kwargs), sort_keys=True, default=str).encode()
        ).hexdigest()

# Callback для сбора метрик
def collect_metrics(metrics: APICallMetrics):
    """Сохраняет метрики в базу данных или систему мониторинга"""
    print(f"📊 Metrics: {metrics}")

# Использование
api_decorator = AIAPIDecorator(
    max_retries=3,
    cache_enabled=True,
    log_enabled=True,
    metrics_callback=collect_metrics
)

@api_decorator
def call_gpt4(prompt: str, temperature: float = 0.7) -> str:
    """Production API вызов с полным набором функций"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content

# Использование
result1 = call_gpt4("Что такое Python?")  # API вызов
result2 = call_gpt4("Что такое Python?")  # Из кеша
print(f"Размер кеша: {call_gpt4.cache_size()}")
```

## Декораторы методов класса

### @staticmethod, @classmethod, @property

Python предоставляет встроенные декораторы для работы с классами:

```python
class AIModel:
    """Класс для работы с AI моделью"""

    model_name = "gpt-4"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._temperature = 0.7

    @property
    def temperature(self) -> float:
        """Getter для temperature"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        """Setter для temperature с валидацией"""
        if not 0 <= value <= 2:
            raise ValueError("Temperature должна быть между 0 и 2")
        self._temperature = value

    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """Статический метод - не требует экземпляра класса"""
        return len(prompt) > 0 and len(prompt) < 10000

    @classmethod
    def from_env(cls) -> 'AIModel':
        """Классовый метод - альтернативный конструктор"""
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        return cls(api_key)

    def call_api(self, prompt: str) -> str:
        """Обычный метод экземпляра"""
        if not self.validate_prompt(prompt):
            raise ValueError("Невалидный prompt")
        # API вызов
        return f"Response for: {prompt}"

# Использование
model = AIModel.from_env()  # Классовый метод
print(AIModel.validate_prompt("Hello"))  # Статический метод
model.temperature = 0.9  # Property setter
print(model.temperature)  # Property getter
```

## Best Practices

### 1. **Всегда используйте @wraps**
```python
from functools import wraps

def good_decorator(func):
    @wraps(func)  # ✅ Сохраняет метаданные
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 2. **Делайте декораторы конфигурируемыми**
```python
def configurable_decorator(param1="default", param2=10):
    """Декоратор с параметрами"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Используем param1 и param2
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. **Обрабатывайте исключения правильно**
```python
def safe_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise  # ✅ Пробрасываем исключение дальше
    return wrapper
```

### 4. **Документируйте ваши декораторы**
```python
def well_documented_decorator(timeout: int = 30):
    """
    Добавляет timeout к функции

    Args:
        timeout: Максимальное время выполнения в секундах

    Returns:
        Декорированная функция с timeout

    Raises:
        TimeoutError: Если функция выполняется дольше timeout

    Example:
        @well_documented_decorator(timeout=10)
        def slow_function():
            time.sleep(5)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Implementation
            pass
        return wrapper
    return decorator
```

### 5. **Предоставляйте доступ к оригинальной функции**
```python
def transparent_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.__wrapped__ = func  # ✅ Доступ к оригинальной функции
    return wrapper

@transparent_decorator
def my_function():
    pass

# Доступ к оригинальной функции
original = my_function.__wrapped__
```

## Типичные ошибки и как их избежать

### Ошибка 1: Забыли @wraps
```python
# ❌ ПЛОХО
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """Документация"""
    pass

print(my_func.__name__)  # wrapper (неправильно!)

# ✅ ХОРОШО
from functools import wraps

def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func():
    """Документация"""
    pass

print(my_func.__name__)  # my_func (правильно!)
```

### Ошибка 2: Неправильный порядок декораторов
```python
# ❌ ПЛОХО - measure_time будет измерять время кеша
@measure_time
@cache_results
def api_call():
    pass

# ✅ ХОРОШО - measure_time измеряет реальное время API
@cache_results
@measure_time
def api_call():
    pass
```

### Ошибка 3: Изменяемые значения по умолчанию
```python
# ❌ ПЛОХО
def bad_cache_decorator(func, cache={}):  # Мутабельный default!
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# ✅ ХОРОШО
def good_cache_decorator(func):
    cache = {}  # Создаётся при каждом вызове декоратора
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

## Реальный пример: Декоратор для OpenAI API с метриками

```python
from functools import wraps
import time
import logging
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class OpenAICallStats:
    """Статистика вызовов OpenAI API"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    total_duration: float = 0.0
    calls_history: list = field(default_factory=list)

class OpenAIDecorator:
    """Комплексный декоратор для OpenAI API"""

    def __init__(self):
        self.stats = OpenAICallStats()
        self.logger = logging.getLogger(__name__)

    def monitor(
        self,
        model_pricing: dict = {"input": 0.03/1000, "output": 0.06/1000}
    ):
        """
        Декоратор для мониторинга OpenAI вызовов

        Args:
            model_pricing: Цены на токены (input и output на 1000 токенов)
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.stats.total_calls += 1
                start_time = time.time()

                try:
                    # Вызов функции
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time

                    # Извлекаем метаданные из response (если это OpenAI response)
                    if hasattr(result, 'usage'):
                        input_tokens = result.usage.prompt_tokens
                        output_tokens = result.usage.completion_tokens
                        total_tokens = result.usage.total_tokens

                        # Рассчитываем стоимость
                        cost = (
                            input_tokens * model_pricing["input"] +
                            output_tokens * model_pricing["output"]
                        )

                        self.stats.total_tokens += total_tokens
                        self.stats.total_cost += cost

                        # Логируем детали
                        self.logger.info(
                            f"✅ {func.__name__}: {duration:.2f}s, "
                            f"{total_tokens} tokens, ${cost:.4f}"
                        )

                    self.stats.successful_calls += 1
                    self.stats.total_duration += duration

                    # Сохраняем в историю
                    self.stats.calls_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "function": func.__name__,
                        "duration": duration,
                        "success": True
                    })

                    return result

                except Exception as e:
                    duration = time.time() - start_time
                    self.stats.failed_calls += 1
                    self.stats.total_duration += duration

                    self.logger.error(f"❌ {func.__name__} failed: {e}")

                    self.stats.calls_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "function": func.__name__,
                        "duration": duration,
                        "success": False,
                        "error": str(e)
                    })

                    raise

            return wrapper
        return decorator

    def get_report(self) -> str:
        """Генерирует отчёт по статистике"""
        if self.stats.total_calls == 0:
            return "Нет данных для отчёта"

        success_rate = (self.stats.successful_calls / self.stats.total_calls) * 100
        avg_duration = self.stats.total_duration / self.stats.total_calls

        return f"""
╔══════════════════════════════════════╗
║     OpenAI API Call Statistics       ║
╚══════════════════════════════════════╝

📊 Общая статистика:
   • Всего вызовов: {self.stats.total_calls}
   • Успешных: {self.stats.successful_calls}
   • Неудачных: {self.stats.failed_calls}
   • Success Rate: {success_rate:.1f}%

⏱️  Производительность:
   • Общее время: {self.stats.total_duration:.2f}s
   • Среднее время: {avg_duration:.2f}s

🎯 Токены и стоимость:
   • Всего токенов: {self.stats.total_tokens:,}
   • Общая стоимость: ${self.stats.total_cost:.4f}
   • Средняя стоимость: ${self.stats.total_cost/self.stats.successful_calls:.4f}
        """

# Использование
monitor = OpenAIDecorator()

@monitor.monitor(model_pricing={"input": 0.03/1000, "output": 0.06/1000})
def chat_completion(prompt: str):
    """Обёрнутый API вызов"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

# Выполняем несколько вызовов
chat_completion("Что такое Python?")
chat_completion("Что такое AI?")
chat_completion("Что такое ML?")

# Получаем отчёт
print(monitor.get_report())
```

## Заключение

Декораторы — это мощный инструмент Python, который позволяет:

✅ **Переиспользовать код** — одна логика применяется ко многим функциям
✅ **Разделять ответственность** — функция делает одно, декоратор добавляет дополнительную функциональность
✅ **Улучшать читаемость** — декларативный подход делает код понятнее
✅ **Упрощать тестирование** — логику декоратора можно тестировать отдельно
✅ **Стандартизировать паттерны** — единообразная обработка ошибок, логирование, кеширование

Для AI Engineer декораторы особенно важны при работе с:
- API вызовами (retry, rate limiting, кеширование)
- Логированием и мониторингом
- Измерением производительности
- Валидацией данных
- Управлением стоимостью запросов

**Главное правило**: Используйте декораторы для cross-cutting concerns (сквозной функциональности), которая применяется ко многим функциям.

## Дополнительные ресурсы

- [PEP 318 - Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)
- [Real Python: Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity]] - практическое применение декораторов для retry-логики

---

*Эта заметка создана для AI Engineers, работающих с Python и языковыми моделями.*
