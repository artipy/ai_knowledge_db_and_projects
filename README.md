# Knowledge Library: LLM & AI APIs

Персональная база знаний об использовании больших языковых моделей (LLM) и работе с AI API. Репозиторий организован как Obsidian vault с двунаправленными ссылками между заметками и содержит как теоретические материалы, так и практические задания.

## 📚 О репозитории

Этот репозиторий представляет собой структурированную коллекцию знаний о:
- Работе с OpenAI API и совместимыми сервисами
- Техниках промпт-инжиниринга
- Работе с Hugging Face: Pipeline API, Auto-классы, Document QA
- Локальном развертывании LLM моделей
- Python инструментах для AI engineers (декораторы, retry-логика, обработка ошибок)
- Практическом применении AI в задачах обработки текста

**Язык контента:** Русский
**Язык именования файлов:** Английский
**Формат:** Markdown с Obsidian-синтаксисом для ссылок

## 🗂️ Структура репозитория

```
knowledge_lib/
├── OpenAI_API/                    # Работа с OpenAI API
│   ├── Introduction_to_OpenAI_API.md
│   ├── Working_with_OpenAI_API_in_Python.md
│   ├── Chat_Roles_and_Multi_Turn_Conversations.md
│   ├── Structuring_End_to_End_Applications.md
│   ├── Function_Calling.md
│   ├── Best_Practices_for_Production_Applications.md
│   ├── Working_with_Embeddings.md
│   ├── Embeddings_Applications.md
│   └── Vector_Databases_with_ChromaDB.md
│
├── Prompt_Engineering/            # Техники промпт-инжиниринга
│   ├── Prompt_Engineering_Best_Practices.md
│   ├── Advanced_Prompt_Engineering_Strategies.md
│   ├── Prompt_Engineering_for_Business_Applications.md
│   └── Prompt_Engineering_for_Chatbot_Development.md
│
├── Hugging_Face/                  # Работа с Hugging Face
│   ├── Getting_Started_with_Hugging_Face.md
│   └── Building_Pipelines_with_Hugging_Face.md
│
├── LLMOps/                        # LLMOps практики и жизненный цикл LLM
│   ├── Introduction_to_LLMOps_and_Ideation_Phase.md
│   └── Development_Phase.md
│
├── Local_LLM_Deployment/          # Локальное развертывание моделей
│   └── Local_LLM_Deployment_with_LM_Studio.md
│
├── Python_for_AI/                 # Python инструменты для AI engineers
│   ├── Python_Decorators.md
│   └── Tenacity_Library_for_Retry_Logic.md
│
├── Exercises/                     # Практические задания
│   ├── README.md
│   ├── 01_OpenAI_API_Text_Processing_Exercise.md
│   ├── 02_Chat_Roles_and_Conversations_Exercise.md
│   ├── 03_Prompt_Engineering_Exercise.md
│   ├── 04_Advanced_Prompt_Engineering_Strategies_Exercise.md
│   ├── 05_Business_Applications_Prompt_Engineering_Exercise.md
│   ├── 06_Prompt_Engineering_for_Chatbots_Exercise.md
│   ├── 07_Structuring_End_to_End_Applications_Exercise.md
│   ├── 08_Function_Calling_Exercise.md
│   ├── 09_Working_with_Embeddings_Exercise.md
│   ├── 10_Embeddings_Applications_Exercise.md
│   ├── 11_Vector_Databases_with_ChromaDB_Exercise.md
│   ├── Solves/                    # Решения заданий (.ipynb)
│   │   ├── 01_OpenAI_API_Text_Processing_Solve.ipynb
│   │   ├── 02_Chat_Roles_and_Conversations_Solve.ipynb
│   │   └── ... (10 solutions total)
│   └── Reviews/                   # Проверки решений (*_Review.md)
│       ├── 01_OpenAI_API_Text_Processing_Review.md
│       ├── 02_Chat_Roles_and_Conversations_Review.md
│       └── ... (10 reviews total)
│
├── raw_notes/                     # Необработанные материалы
│   └── *.ipynb                    # Jupyter notebooks для обработки
│
└── .obsidian/                     # Конфигурация Obsidian
```

## 🎯 Основные темы

### OpenAI API
- Базовое подключение и аутентификация
- Работа с различными провайдерами (OpenAI, Gemini, OpenRouter)
- Обработка текста: редактирование, резюмирование, генерация
- Управление параметрами: `temperature`, `max_completion_tokens`
- Расчет стоимости запросов
- Система ролей в чатах: system, user, assistant
- Многоэтапные диалоги с сохранением контекста (multi-turn conversations)
- Управление поведением модели через системные сообщения
- Function calling: определение функций, извлечение структурированных данных, параллельный вызов, `tool_choice`, интеграция с внешними API
- Embeddings: векторные представления текста, пакетная обработка, косинусное сходство, семантический поиск, классификация без обучения, визуализация t-SNE; практические применения: обогащённые эмбеддинги, системы рекомендаций (одиночные и по истории просмотров с усреднением векторов), zero-shot классификация с описаниями классов
- Векторные базы данных с ChromaDB: PersistentClient, создание коллекций с функцией эмбеддингов, CRUD-операции (add/get/update/upsert/delete), семантический поиск через query, несколько запросов одним вызовом, фильтрация по метаданным с операторами `$eq/$ne/$gt/$lt/$and/$or`, оценка стоимости через tiktoken
- Лучшие практики для production: модерация контента (safe/unsafe классификация, guardrails), валидация модели (adversarial testing, обнаружение сарказма), безопасность (идентификация пользователей через UUID, защита API-ключей)

### Prompt Engineering
**Базовые практики:**
- Ключевые принципы создания эффективных промптов
- Использование глаголов действия и детальных инструкций
- Структурирование промптов по разделам
- Генерация форматированных ответов (таблицы, списки, параграфы)
- Пользовательские форматы вывода
- Условная логика в промптах
- Итеративная разработка и улучшение промптов

**Продвинутые стратегии:**
- **Shot Prompting**: Zero-shot, One-shot, Few-shot техники с примерами
- **Multi-Step Prompting**: Пошаговые инструкции для структурированного выполнения задач
- **Chain-of-Thought (CoT)**: Получение пошаговых рассуждений модели для проверки логики
- **Self-Consistency**: Повышение надежности через множественные независимые решения
- **Iterative Refinement**: Циклическое улучшение промптов на основе анализа результатов
- Комбинирование техник для сложных задач
- Few-shot через user-assistant диалоги

**Практическое применение для бизнеса:**
- **Резюмирование и расширение текста**: Обработка отзывов, создание маркетинговых материалов, генерация email-сообщений
- **Трансформация текста**: Перевод на множество языков, изменение тона (формальный/неформальный), улучшение грамматики и читаемости
- **Анализ текста**: Sentiment analysis, классификация по категориям, извлечение сущностей (entity extraction), обработка тикетов поддержки
- **Генерация и объяснение кода**: Создание кода из описания задачи, модификация существующего кода, пошаговые объяснения алгоритмов
- Управление temperature для разных типов задач, обработка ошибок, расчет стоимости и ROI

**Разработка чатботов:**
- **Определение роли и цели**: Правильное позиционирование чатбота через system prompt
- **Настройка поведения**: Управление тональностью, длиной ответов, структурой общения
- **Установка границ**: Определение области компетенции, обработка вопросов вне темы
- **Role-playing prompts**: Использование ролевых промптов для придания характера чатботу
- **Включение внешнего контекста**: Встраивание баз знаний, каталогов, FAQ в system prompt
- **Мультиязычная поддержка**: Автоматическое определение языка и ответы на соответствующем языке
- Комплексные чатботы с условной логикой и многошаговыми диалогами

### LLMOps

- **Обзор LLMOps**: Практики и инфраструктура для управления LLM-приложениями на всех этапах жизненного цикла
- **LLMOps vs MLOps**: Сравнение подходов по размеру модели, данным, предсказуемости и способам улучшения
- **Жизненный цикл LLM**: Три фазы — Ideation → Development → Operation — с возможностью нелинейных итераций
- **Фаза идеации**: Оценка данных (соответствие, доступность, стандартизация), выбор базовой модели
- **Выбор модели**: Проприетарные vs Open-Source — преимущества, недостатки, ключевые факторы (производительность, лицензии, стоимость)
- **Фаза разработки**: Prompt Engineering (структура промпта, управление промптами, шаблоны), Chains & Agents (детерминированные vs адаптивные архитектуры), RAG (векторные БД, embeddings) vs Fine-tuning (Supervised FT, RLHF), Testing (статистический, LLM-as-a-Judge, категориальный)

### Hugging Face

- **Pipeline API**: Высокоуровневый интерфейс для быстрого запуска NLP-моделей
- **Классификация текста**: Sentiment analysis, проверка грамматики, QNLI, Zero-Shot классификация
- **Резюмирование текста**: Экстрактивный и абстрактивный подходы, управление длиной ответа
- **Auto-классы и токенизаторы**: Гибкая загрузка моделей с полным контролем над инференсом
- **Document QA**: Ответы на вопросы по PDF-документам с использованием pypdf
- **InferenceClient**: Удалённый запуск моделей через провайдеров без локальных ресурсов
- **Датасеты**: Работа с Hugging Face Datasets, формат Apache Arrow, фильтрация и выборка

### Python для AI Engineers
- **Декораторы**: Функции высшего порядка, @wraps, параметризованные декораторы
- **Практические декораторы**: Логирование, измерение времени, кеширование, валидация типов, rate limiting
- **Библиотека Tenacity**: Retry-логика для устойчивой работы с API
- **Обработка ошибок**: Rate limits, сетевые сбои, таймауты, экспоненциальная задержка
- **Production patterns**: Метрики, мониторинг, fallback стратегии, асинхронные вызовы
- **Кеширование и оптимизация**: Экономия средств на повторных запросах к LLM

### Практические навыки
- Построение пайплайнов обработки текста
- Работа с токенами и оптимизация стоимости
- Интеграция LLM в приложения
- Создание production-ready обёрток для AI API

## 📖 Как использовать

### Для изучения теории

1. Начните с базовых заметок в директориях по темам
2. Следуйте по ссылкам `[[Note_Name]]` для углубления в связанные темы
3. Все заметки связаны двунаправленными ссылками для удобной навигации

**Рекомендуемый порядок изучения:**
1. `OpenAI_API/Introduction_to_OpenAI_API.md` - базовое введение
2. `OpenAI_API/Working_with_OpenAI_API_in_Python.md` - практические примеры
3. `Python_for_AI/Python_Decorators.md` - основы декораторов для AI разработки
4. `Python_for_AI/Tenacity_Library_for_Retry_Logic.md` - устойчивая работа с API
5. `OpenAI_API/Chat_Roles_and_Multi_Turn_Conversations.md` - роли в чатах и создание диалогов
6. Выполнить `Exercises/01_OpenAI_API_Text_Processing_Exercise.md`

### Для практики

1. Откройте `Exercises/README.md` для списка доступных заданий
2. Каждое задание содержит:
   - Четкие цели обучения
   - Пошаговые инструкции
   - Шаблоны кода
   - Критерии оценки
   - Ожидаемые результаты
3. Решения сохраняйте в `Exercises/Solves/` как Jupyter notebooks

### Для работы в Obsidian

```bash
# Откройте директорию как vault в Obsidian
# Файл → Open vault → knowledge_lib/
```

Преимущества Obsidian:
- Визуализация связей между заметками (граф знаний)
- Быстрая навигация по ссылкам
- Предварительный просмотр связанных заметок

### Для углубленного изучения Python

Рекомендуется изучить заметки в `Python_for_AI/` перед началом работы с API:
- Декораторы помогут понять, как работают библиотеки типа tenacity
- Retry-логика критична для production систем с AI API
- Все паттерны применимы к реальным проектам

## 🛠️ Технические требования

### Для просмотра заметок
- Любой Markdown-редактор или Obsidian

### Для выполнения заданий
```bash
# Установка зависимостей
pip install openai python-dotenv tenacity

# Создание .env файла с API ключами
echo "GEMINI_TOKEN=your_api_key" > .env
echo "BASE_URL=your_base_url" >> .env
echo "BASE_MODEL=your_model" >> .env
```

## 📝 Соглашения об именовании

### Заметки
- Формат: `Topic_Name.md`
- Примеры: `Introduction_to_OpenAI_API.md`, `Working_with_OpenAI_API_in_Python.md`

### Задания
- Формат: `##_Topic_Name_Exercise.md`
- Решения: `##_Topic_Name_Solve.ipynb`
- Проверки: `##_Topic_Name_Review.md`

### Директории
- Формат: `Topic_Name/` с подчеркиваниями
- Примеры: `OpenAI_API/`, `Local_LLM_Deployment/`

## 🔗 Система ссылок

Используется синтаксис Obsidian для внутренних ссылок:

```markdown
[[Note_Name]]                          # Простая ссылка
[[Folder/Note_Name]]                   # Ссылка с путем
[[Note_Name|Отображаемый текст]]       # Ссылка с алиасом
```

**Важно:** Все заметки (кроме `raw_notes/`) должны иметь двунаправленные ссылки для построения связного графа знаний.

## 📊 Статус заданий

| № | Название | Тема | Сложность | Время | Решение | Ревью |
|---|----------|------|-----------|-------|---------|-------|
| 01 | Text Processing with OpenAI API | OpenAI API | Начальный | ~75 мин | ✅ | ✅ |
| 02 | Chat Roles and Conversations | Роли в чатах | Начальный | ~80 мин | ✅ | ✅ |
| 03 | Prompt Engineering Best Practices | Prompt Engineering | Начальный | ~90 мин | ✅ | ✅ |
| 04 | Advanced Prompt Engineering Strategies | Продвинутый Prompt Engineering | Средний | ~120 мин | ✅ | ✅ |
| 05 | Business Applications Prompt Engineering | Практическое применение для бизнеса | Средний | ~95 мин | ✅ | ✅ (v4) |
| 06 | Prompt Engineering for Chatbots | Разработка чатботов | Средний | ~110 мин | ✅ | ✅ |
| 07 | Structuring End-to-End Applications | Production API паттерны | Средний | ~100 мин | ✅ | ✅ |
| 08 | Function Calling | Function calling и интеграция с API | Средний | ~95 мин | ✅ | ✅ |
| 09 | Working with Embeddings | Embeddings и семантический поиск | Средний | ~100 мин | ✅ | ✅ |
| 10 | Embeddings Applications | Поиск, рекомендации, zero-shot классификация | Средний | ~100 мин | ✅ | ✅ (v3) |
| 11 | Vector Databases with ChromaDB | ChromaDB, CRUD, семантический поиск, фильтрация | Средний | ~100 мин | ⬜ | ⬜ |

## 🚀 Roadmap

### Планируемые темы
- [x] Python декораторы для AI разработки
- [x] Retry-логика и обработка ошибок (Tenacity)
- [x] Advanced Prompt Engineering техники (Shot Prompting, Chain-of-Thought, Self-Consistency)
- [x] Работа с эмбеддингами
- [x] Векторные базы данных с ChromaDB
- [x] Function calling и Tool use
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Fine-tuning моделей
- [ ] Оценка качества и benchmarking
- [ ] Асинхронная работа с API (asyncio, aiohttp)
- [ ] Streaming responses и real-time обработка

### Планируемые задания
- [x] Построение чат-ботов с контекстом
- [x] Создание специализированных чатботов с ролями и ограничениями
- [x] Production-ready API паттерны (JSON, ошибки, батчинг, retry, токены)
- [ ] Классификация и анализ настроений (advanced)
- [ ] Работа с большими документами
- [ ] Создание специализированных ассистентов с RAG

## 📄 Лицензия и использование

Этот репозиторий создан в образовательных целях. Материалы можно свободно использовать для обучения.

## 🤝 Структура работы

1. **Сырые материалы** → `raw_notes/` (Jupyter notebooks, черновики)
2. **Обработка** → Создание структурированных заметок в тематических папках
3. **Создание заданий** → `Exercises/` с критериями оценки
4. **Решение** → `Exercises/Solves/` решения в формате .ipynb
5. **Проверка** → `Exercises/Reviews/` детальные разборы с оценками

## 📌 Дополнительная информация

- Все настройки для работы с репозиторием описаны в `CLAUDE.md`
- История изменений доступна через git log
- Для вопросов и предложений используйте Issues

---

**Последнее обновление:** 2026-03-14
**Количество заметок:** 21 основная (9 OpenAI API, 4 Prompt Engineering, 2 Hugging Face, 2 LLMOps, 1 Local LLM, 2 Python for AI)
**Количество заданий:** 11 (задания 01-10 с решениями и ревью; задание 11 — без решения)
**Статус:** Активная разработка
