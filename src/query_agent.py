from dataclasses import dataclass
from typing import Any, List, Sequence

from weaviate.agents.classes import ChatMessage, QueryAgentCollectionConfig
from weaviate.agents.query import QueryAgent
from weaviate.classes.query import Filter

from collection_config import (
    COURSE_VIEW_PROPERTIES,
    COURSES_COLLECTION,
    INSTRUCTORS_COLLECTION,
    query_agent_collections,
)
from project_config import connect_weaviate_client, load_environment_config


SYSTEM_PROMPT = """
You are a university academic assistant.
Answer clearly and concretely, based only on data retrieved from Weaviate.
If data is missing, say that explicitly.
Keep answers concise but informative.
""".strip()


@dataclass
class QueryResult:
    final_answer: str
    selected_collections: List[str]


class UniversityQueryAssistant:
    def __init__(self) -> None:
        config = load_environment_config()
        self.client = connect_weaviate_client(config)

        self.base_collections = query_agent_collections()

        self.query_agent = QueryAgent(
            client=self.client,
            collections=self.base_collections,
            system_prompt=SYSTEM_PROMPT,
            timeout=120,
        )

    def close(self) -> None:
        self.client.close()

    def _infer_collections(self, question: str) -> List[str]:
        q = question.lower()

        instructor_keywords = {
            "instructor",
            "professor",
            "teacher",
            "lecturer",
            "bio",
            "research",
            "experience",
            "who teaches",
        }
        course_keywords = {
            "course",
            "courses",
            "ects",
            "semester",
            "skills",
            "program",
            "subject",
            "class",
        }

        has_instructor = any(keyword in q for keyword in instructor_keywords)
        has_course = any(keyword in q for keyword in course_keywords)

        if has_instructor and not has_course:
            return [INSTRUCTORS_COLLECTION]
        if has_course and not has_instructor:
            return [COURSES_COLLECTION]
        return [COURSES_COLLECTION, INSTRUCTORS_COLLECTION]

    def ask(self, question: str) -> QueryResult:
        selected = self._infer_collections(question)
        response = self.query_agent.ask(question, collections=selected)
        return QueryResult(final_answer=response.final_answer, selected_collections=selected)

    def ask_conversation(self, history: Sequence[ChatMessage]) -> QueryResult:
        response = self.query_agent.ask(list(history))
        return QueryResult(
            final_answer=response.final_answer,
            selected_collections=[COURSES_COLLECTION, INSTRUCTORS_COLLECTION],
        )

    def search(self, question: str, limit: int = 5):
        selected = self._infer_collections(question)
        response = self.query_agent.search(question, limit=limit, collections=selected)
        return response, selected

    def ask_follow_up(self, history: Sequence[ChatMessage], user_message: str) -> QueryResult:
        conversation = list(history)
        conversation.append(ChatMessage(role="user", content=user_message))
        return self.ask_conversation(conversation)

    def ask_with_english_courses_filter(self, question: str) -> QueryResult:
        filtered_courses = QueryAgentCollectionConfig(
            name=COURSES_COLLECTION,
            view_properties=COURSE_VIEW_PROPERTIES,
            additional_filters=Filter.by_property("language").equal("English"),
        )

        response = self.query_agent.ask(
            question,
            collections=[filtered_courses, INSTRUCTORS_COLLECTION],
        )
        return QueryResult(
            final_answer=response.final_answer,
            selected_collections=[
                f"{COURSES_COLLECTION} (language=English)",
                INSTRUCTORS_COLLECTION,
            ],
        )


def format_search_response(search_response: Any) -> str:
    lines: List[str] = []

    objects = getattr(search_response.search_results, "objects", [])
    if not objects:
        return "No objects found."

    for index, obj in enumerate(objects, start=1):
        props = obj.properties or {}
        title = props.get("title") or props.get("full_name") or "N/A"
        summary = props.get("description") or props.get("bio") or ""
        lines.append(f"{index}. {title}")
        if summary:
            lines.append(f"   - {summary}")

    return "\n".join(lines)
