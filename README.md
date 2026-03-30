# AI-agent-system

## Project scope

This repository currently implements:

- **Part 1**: Data modeling and loading in Weaviate
- **Part 2**: Query Agent with required query scenarios
- **Part 3**: Interface and user experience via Streamlit UI
- **Part 6**: Personalization Agent extension

## Requirements

- Python 3.10+
- Weaviate Cloud cluster
- API keys configured in environment variables

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment setup

Copy `.env.example` to `.env` and fill in real values:

```dotenv
WEAVIATE_URL=https://your-cluster-id.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
LLM_PROVIDER=openai
RESET_COLLECTIONS=true
```

`RESET_COLLECTIONS=true` will delete and recreate `Courses` and `Instructors` before loading.

To use Gemini instead of OpenAI, set:

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
```
## Run data modeling + import

```bash
python src/load_data.py
```

If you changed `LLM_PROVIDER`, keep `RESET_COLLECTIONS=true` for one run so collections are recreated with the matching vectorizer/provider config.

Successful run will:

1. Connect to Weaviate Cloud
2. Create collection schemas (`Courses`, `Instructors`) if missing
3. Import instructors from `src/data/instructors.json`
4. Import courses from `src/data/courses.json`

## Dataset

- `src/data/courses.json`
- `src/data/instructors.json`

Domain used: **University courses**.

## Project structure

- `src/project_config.py` - shared env/config and Weaviate client setup
- `src/collection_config.py` - shared collection names and schema/view properties
- `src/demo_queries.py` - shared required demo questions
- `src/load_data.py` - collection creation + data import
- `src/query_agent.py` - Query Agent assistant logic
- `src/query_agent_demo.py` - 5-query CLI demonstration
- `src/app.py` - Streamlit chat UI
- `src/personalization_profiles.py` - persona profiles and seeded preferences
- `src/personalization_agent.py` - Personalization Agent integration
- `src/personalization_demo.py` - personalized recommendation demo

See additional structure notes in `docs/project_structure.md`.

## Query Agent (Part 2)

Implemented files:

- `src/query_agent.py` - Query Agent assistant logic
- `src/query_agent_demo.py` - required 5-query demonstration

### What is implemented

The assistant:

- accepts natural-language questions
- picks one collection or both (`Courses`, `Instructors`) based on question intent
- returns a clear generated answer via Weaviate Query Agent

### Run Query Agent demo (5 required query types)

```bash
python src/query_agent_demo.py
```

Demo includes:

1. ordinary search
2. multi-collection query
3. follow-up query
4. filtering + aggregation-style query
5. free-form natural-language query

### Notes

- Query Agent requires Weaviate Cloud and valid API keys.
- Install dependencies with:

```bash
pip install -r requirements.txt
```

## Interface & UX (Part 3)

Implemented file:

- `src/app.py` - Streamlit UI for the university assistant

### UI features

- chat-based interface for natural-language questions
- query modes:
	- `Ask`
	- `Search`
	- `Ask (English courses filter)`
- one-click preset demo queries (all 5 required scenarios)
- conversational follow-up support (multi-turn context)
- selected collections shown under each response for transparency

### Run the UI

```bash
streamlit run src/app.py
```

## Demonstration clarity (Part 5)

Presentation assets:

- `docs/demo_presentation_bg.md` - ready Bulgarian presentation script
- `src/demo_check.py` - quick readiness check before presentation

Run pre-demo check:

```bash
python src/demo_check.py
```

## Personalization extension (Part 6)

Implemented files:

- `src/personalization_profiles.py`
- `src/personalization_agent.py`
- `src/personalization_demo.py`

Implemented functionality:

- create/connect Weaviate `PersonalizationAgent` on `Courses`
- persona upsert with profile properties
- interaction sync from seeded likes/dislikes
- personalized recommendations with agent ranking + rationale
- UI integration via `Personalized Recommendations` mode

Run personalization demo:

```bash
python src/personalization_demo.py
```
