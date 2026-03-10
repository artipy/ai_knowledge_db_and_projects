# Практические задания

Эта директория содержит практические задания для проверки и закрепления знаний по различным темам базы знаний.

## Структура заданий

Каждое задание имеет номер и описательное название на английском языке:
- `01_OpenAI_API_Text_Processing_Exercise.md` - базовая работа с OpenAI API (редактирование, резюмирование, генерация текста)
- `02_Chat_Roles_and_Conversations_Exercise.md` - система ролей и многоэтапные диалоги
- `03_Prompt_Engineering_Exercise.md` - лучшие практики создания эффективных промптов
- `04_Advanced_Prompt_Engineering_Strategies_Exercise.md` - продвинутые стратегии (Shot Prompting, Chain-of-Thought, Self-Consistency)
- `05_Business_Applications_Prompt_Engineering_Exercise.md` - применение промпт-инжиниринга для бизнес-задач
- `06_Prompt_Engineering_for_Chatbots_Exercise.md` - создание специализированных чатботов с ролями и контекстом
- `07_Structuring_End_to_End_Applications_Exercise.md` - production-ready паттерны: структурированный JSON, обработка ошибок, батчинг, retry-логика, подсчёт токенов
- `08_Function_Calling_Exercise.md` - function calling: определение функций, извлечение данных, параллельный вызов, tool_choice, интеграция с внешним API

### Директории для решений и проверок

**`Solves/`** - решения заданий:
- Формат: `##_Topic_Name_Solve.ipynb`
- Содержит: код решений в формате Jupyter notebook с выполненными ячейками

**`Reviews/`** - проверки решений:
- Формат: `##_Topic_Name_Review.md`
- Содержит: детальные разборы с оценками, анализом ошибок и рекомендациями

## Формат заданий

Каждое задание включает:
- 📋 **Цель задания** - что вы научитесь делать
- 📚 **Связанные материалы** - ссылки на теоретические заметки
- ⚙️ **Предварительные требования** - что нужно установить/настроить
- 📝 **Пошаговые задачи** - четкие инструкции для выполнения
- ✅ **Ожидаемые результаты** - как должен выглядеть правильный ответ
- 💻 **Шаблоны кода** - заготовки для ускорения работы
- 📊 **Критерии оценки** - как оценить качество выполнения
- 💡 **Рекомендации** - советы по выполнению

## Как использовать

1. Выберите задание, соответствующее изученному материалу
2. Прочитайте связанные теоретические заметки
3. Подготовьте окружение (установите библиотеки, создайте файлы)
4. Выполняйте задачи последовательно
5. Сравните ваши результаты с ожидаемыми
6. Экспериментируйте и анализируйте результаты

## Список доступных заданий

| № | Название | Тема | Сложность | Время | Решение | Ревью |
|---|----------|------|-----------|-------|---------|-------|
| 01 | [Text Processing with OpenAI API](01_OpenAI_API_Text_Processing_Exercise.md) | OpenAI API | Начальный | ~75 мин | [✅](Solves/01_OpenAI_API_Text_Processing_Solve.ipynb) | [✅](Reviews/01_OpenAI_API_Text_Processing_Review.md) |
| 02 | [Chat Roles and Conversations](02_Chat_Roles_and_Conversations_Exercise.md) | Роли в чатах | Начальный | ~80 мин | [✅](Solves/02_Chat_Roles_and_Conversations_Solve.ipynb) | [✅](Reviews/02_Chat_Roles_and_Conversations_Review.md) |
| 03 | [Prompt Engineering Best Practices](03_Prompt_Engineering_Exercise.md) | Prompt Engineering | Начальный | ~90 мин | [✅](Solves/03_Prompt_Engineering_Solves.ipynb) | [✅](Reviews/03_Prompt_Engineering_Review.md) |
| 04 | [Advanced Prompt Engineering Strategies](04_Advanced_Prompt_Engineering_Strategies_Exercise.md) | Advanced Prompt Engineering | Средний | ~120 мин | [✅](Solves/04_Advanced_Prompt_Engineering_Strategies_Solve.ipynb) | [✅](Reviews/04_Advanced_Prompt_Engineering_Strategies_Review.md) |
| 05 | [Business Applications Prompt Engineering](05_Business_Applications_Prompt_Engineering_Exercise.md) | Практическое применение | Средний | ~95 мин | [✅](Solves/05_Business_Applications_Prompt_Engineering_Solve.ipynb) | [✅](Reviews/05_Business_Applications_Prompt_Engineering_Review_v4.md) |
| 06 | [Prompt Engineering for Chatbots](06_Prompt_Engineering_for_Chatbots_Exercise.md) | Разработка чатботов | Средний | ~110 мин | [✅](Solves/06_Prompt_Engineering_for_Chatbots_Solve.ipynb) | [✅](Reviews/06_Prompt_Engineering_for_Chatbots_Review.md) |
| 07 | [Structuring End-to-End Applications](07_Structuring_End_to_End_Applications_Exercise.md) | Production API паттерны | Средний | ~100 мин | [✅](Solves/07_Structuring_End_to_End_Applications_Solve.ipynb) | [✅](Reviews/07_Structuring_End_to_End_Applications_Review.md) |
| 08 | [Function Calling](08_Function_Calling_Exercise.md) | Function calling и интеграция с API | Средний | ~95 мин | [✅](Solves/08_Function_Calling_Solve.ipynb) | [✅](Reviews/08_Function_Calling_Review.md) |

## Описание заданий

### 01. Text Processing with OpenAI API

**Что вы освоите:**
- Редактирование и трансформация текстов через API
- Резюмирование больших объемов информации
- Расчет и оптимизация стоимости запросов
- Управление параметром `temperature` для контроля креативности
- Zero-shot и Few-shot промптинг для классификации

**Предварительные требования:** Базовое понимание Python, установленные библиотеки `openai` и `python-dotenv`

**Связанные заметки:**
- [[OpenAI_API/Introduction_to_OpenAI_API|Введение в OpenAI API]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]
- [[Python_for_AI/Python_Decorators|Декораторы в Python]] - для понимания продвинутых паттернов
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity]] - для устойчивой работы с API

---

### 02. Chat Roles and Conversations

**Что вы освоите:**
- Управление поведением модели через системную роль
- Установку границ и ограничений для специализированных чат-ботов
- Few-shot prompting через синтетические диалоги user-assistant
- Создание многоэтапных диалогов с сохранением контекста
- Анализ и оптимизацию стоимости длинных разговоров

**Предварительные требования:** Выполненное задание №01, понимание базовых принципов работы с API

**Связанные заметки:**
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity]] - для обработки ошибок в production

---

### 03. Prompt Engineering Best Practices

**Что вы освоите:**
- Использование эффективных глаголов действия в промптах
- Создание детальных инструкций с учетом аудитории и контекста
- Структурирование промптов для получения форматированных ответов
- Генерацию таблиц, списков и пользовательских форматов
- Встраивание условной логики в промпты
- Итеративное улучшение промптов для достижения лучших результатов
- Применение разделителей и few-shot learning

**Предварительные требования:** Выполненные задания №01 и №02, понимание работы с OpenAI API

**Связанные заметки:**
- [[Prompt_Engineering/Prompt_Engineering_Best_Practices|Лучшие практики Prompt Engineering]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]
- [[Python_for_AI/Python_Decorators|Декораторы в Python]] - для создания переиспользуемых паттернов

---

### 04. Advanced Prompt Engineering Strategies

**Что вы освоите:**
- Shot Prompting: сравнение Zero-shot, One-shot и Few-shot подходов
- Few-shot через user-assistant диалоги для классификации
- Multi-Step Prompting для структурированного выполнения задач
- Chain-of-Thought (CoT) для получения пошаговых рассуждений модели
- Self-Consistency для повышения надежности через множественные решения
- Iterative Refinement - циклическое улучшение промптов
- Комбинирование техник (Multi-Step + CoT + Few-Shot) для сложных задач
- Построение production-ready классификаторов с высокой точностью

**Предварительные требования:** Выполненные задания №01-03, понимание базовых техник prompt engineering

**Связанные заметки:**
- [[Prompt_Engineering/Advanced_Prompt_Engineering_Strategies|Продвинутые стратегии Prompt Engineering]]
- [[Prompt_Engineering/Prompt_Engineering_Best_Practices|Лучшие практики Prompt Engineering]]
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]]

---

### 05. Business Applications Prompt Engineering

**Что вы освоите:**
- Резюмирование и расширение текста для различных целей (отзывы, маркетинг, email)
- Многоэтапную трансформацию текста с chaining промптов
- Адаптацию технического контента для разных аудиторий
- Многоклассовую классификацию (тикеты поддержки по категориям, приоритету, тону)
- Извлечение структурированных данных с few-shot learning
- Генерацию production-ready кода с валидацией и обработкой ошибок
- Объяснение, модификацию и расширение существующего кода
- Построение комплексных пайплайнов обработки данных
- Расчет стоимости и оптимизацию API-вызовов

**Предварительные требования:** Выполненные задания №01-04, понимание продвинутых техник prompt engineering

**Связанные заметки:**
- [[Prompt_Engineering/Prompt_Engineering_for_Business_Applications|Prompt Engineering для бизнес-приложений]]
- [[Prompt_Engineering/Advanced_Prompt_Engineering_Strategies|Продвинутые стратегии Prompt Engineering]]
- [[Prompt_Engineering/Prompt_Engineering_Best_Practices|Лучшие практики Prompt Engineering]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]

---

### 06. Prompt Engineering for Chatbots

**Что вы освоите:**
- Определение роли и цели чатбота через system prompt
- Настройку поведения: тональность, длина ответов, структура общения
- Установку границ и ограничений для предотвращения неправильного использования
- Создание трех версий чатбота с разными тональностями
- Включение внешнего контекста (каталоги товаров, базы знаний)
- Построение комплексных чатботов с условной логикой и многошаговыми диалогами
- Реализацию мультиязычной поддержки с автоматическим определением языка

**Предварительные требования:** Выполненные задания №02 и №05, понимание работы с системными ролями

**Связанные заметки:**
- [[Prompt_Engineering/Prompt_Engineering_for_Chatbot_Development|Prompt Engineering для разработки чатботов]]
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]]
- [[Prompt_Engineering/Prompt_Engineering_Best_Practices|Лучшие практики Prompt Engineering]]

---

### 07. Structuring End-to-End Applications

**Что вы освоите:**
- Запрос и парсинг структурированных JSON-ответов через `response_format`
- Раздельную обработку разных типов ошибок OpenAI API (Auth, RateLimit, BadRequest)
- Логирование запросов с подсчётом использованных токенов
- Оптимизацию числа запросов через батчинг (сравнение одиночных vs. пакетных запросов)
- Реализацию retry-логики с экспоненциальным откатом через `tenacity`
- Объединение `@retry` и `try/except` в production-ready функцию
- Подсчёт токенов до отправки запроса с помощью `tiktoken`
- Построение полного пайплайна обработки текста со всеми перечисленными элементами

**Предварительные требования:** Выполненные задания №1–2, установленные библиотеки `openai`, `python-dotenv`, `tenacity`, `tiktoken`

**Связанные заметки:**
- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]]
- [[OpenAI_API/Working_with_OpenAI_API_in_Python|Работа с OpenAI API в Python]]
- [[Python_for_AI/Tenacity_Library_for_Retry_Logic|Библиотека Tenacity для retry-логики]]
- [[Python_for_AI/Python_Decorators|Декораторы в Python]]

---

### 08. Function Calling

**Что вы освоите:**
- Определение функций с точными схемами параметров и передачу через `tools`
- Извлечение структурированных данных из текста надёжнее, чем через `json_object`
- Параллельный вызов нескольких функций в одном запросе
- Управление выбором функции через `tool_choice` (auto и принудительный)
- Предотвращение домыслов модели с помощью системных сообщений
- Интеграцию OpenAI API с внешними REST API через function calling

**Предварительные требования:** Выполненные задания №01 и №07, установленные библиотеки `openai`, `python-dotenv`, `requests`

**Связанные заметки:**
- [[OpenAI_API/Function_Calling|Вызов функций (Function Calling)]]
- [[OpenAI_API/Structuring_End_to_End_Applications|Структурирование end-to-end приложений]]
- [[OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations|Роли в чатах и многоэтапные диалоги]]

## Рекомендуемый порядок выполнения

```mermaid
graph LR
    A[Задание 01:<br/>Text Processing] --> B[Задание 02:<br/>Chat Roles]
    B --> C[Задание 03:<br/>Prompt Engineering]
    C --> D[Задание 04:<br/>Advanced Strategies]
    D --> E[Задание 05:<br/>Business Applications]
    E --> F[Задание 06:<br/>Chatbot Development]
    F --> G[Задание 07:<br/>End-to-End Applications]
    G --> H[Задание 08:<br/>Function Calling]
    H --> I[Будущие задания]
```

**Важно:** Задания построены с прогрессивным увеличением сложности. Рекомендуется выполнять их последовательно для лучшего усвоения материала.

---

*Задания регулярно обновляются и дополняются новыми по мере развития базы знаний*
