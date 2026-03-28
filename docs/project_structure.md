# Project Structure and Code Quality Notes

This document summarizes architecture decisions made for cleaner structure and easier grading.

## Structure

- `src/project_config.py`
  - Centralized environment loading and Weaviate client initialization.
  - Removes duplicated connection logic across scripts.

- `src/collection_config.py`
  - Shared collection names, schema properties, and Query Agent collection configuration.
  - Keeps schema/view properties consistent in one place.

- `src/demo_queries.py`
  - Single source of truth for the 5 required demo questions.
  - Reused by both CLI demo and Streamlit UI.

- `src/personalization_profiles.py`
  - Defines reusable persona profiles for personalized recommendations.

- `src/personalization_agent.py`
  - Encapsulates Weaviate Personalization Agent lifecycle, persona upsert,
    interaction sync, and recommendation formatting.

- `src/load_data.py`
  - Focused on schema creation and data import only.

- `src/query_agent.py`
  - Focused on Query Agent behavior and query handling logic.

- `src/query_agent_demo.py`
  - Deterministic demonstration script for required scenarios.

- `src/app.py`
  - End-user chat interface for interactive usage.

- `src/personalization_demo.py`
  - Deterministic demonstration script for the extension category.

## Maintainability improvements

- Shared constants and schema definitions reduce copy-paste risk.
- Connection/auth logic is centralized.
- Demo prompts are not duplicated across files.
- Clear separation of concerns between data loading, agent logic, demo flow, and UI.
