# Демонстрация (Part 5) – Ясно представяне

Този документ е кратък сценарий за представяне на проекта пред преподавател.

## 0) Подготовка (1 мин)

1. Покажи `.env` (без да показваш реални ключове).
2. Потвърди, че средата е активна и зависимостите са инсталирани.
3. Кажи домейна: **университетски курсове**.

## 1) Данни и модел (2 мин)

Команда:

```bash
python src/load_data.py
```

Какво казваш:

- „Създавам 2 колекции: Courses и Instructors.“
- „Имам текстови полета за търсене: `description` и `bio`."
- „Зареждам данните от JSON в Weaviate Cloud.“

## 2) Query Agent – 5 задължителни заявки (4–5 мин)

Команда:

```bash
python src/query_agent_demo.py
```

Покриваш последователно:

1. ordinary search
2. multi-collection query
3. follow-up query
4. filtering/aggregation logic
5. free-form query

Какво подчертаваш:

- Agent-ът приема естествен език.
- Избира подходяща колекция/комбинация.
- Връща разбираем отговор.

## 3) UX интерфейс (2–3 мин)

Команда:

```bash
streamlit run src/app.py
```

Покажи в UI:

- чат вход с естествен език;
- режими `Ask`, `Search`, `Ask (English courses filter)`;
- готови demo бутони;
- follow-up поведение в чат;
- видимост на избраните колекции.

## 4) Структура и качество на кода (1 мин)

Покажи накратко:

- `src/project_config.py` (централизирана конфигурация/връзка)
- `src/collection_config.py` (схеми и shared свойства)
- `src/demo_queries.py` (single source of truth за demo заявките)

## 5) Финал (30 сек)

Извод:

- Проектът покрива данни, Query Agent и UX изискванията.
- Решението е модулно и лесно за разширяване с Personalization/Transformation agent.

## 6) Разширение: Personalization Agent (2 мин)

Команда:

```bash
python src/personalization_demo.py
```

Какво казваш:

- „Имам реална интеграция с Weaviate Personalization Agent върху `Courses`."
- „Добавям/обновявам persona профил и interaction-и (likes/dislikes)."
- „Връщам персонализирани препоръки + обяснение за ранкирането (rationale)."

UI демонстрация:

- В `streamlit` избери режим `Personalized Recommendations`.
- Смени профила (`AI Career Starter`, `Backend & Scale Engineer`, `Data Analyst (BG)`) и задай инструкция в свободен текст.
