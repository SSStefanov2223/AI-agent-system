from weaviate.agents.classes import ChatMessage

from demo_queries import DEMO_QUERIES
from query_agent import UniversityQueryAssistant, format_search_response


def run_demo() -> None:
    assistant = UniversityQueryAssistant()

    try:
        print("=== Query Agent Demo (University Courses) ===")

        print("\n1) Ordinary search")
        search_response, selected = assistant.search(DEMO_QUERIES["ordinary_search"], limit=5)
        print(f"Selected collections: {selected}")
        print(format_search_response(search_response))

        print("\n2) Multi-collection question")
        result_multi = assistant.ask(DEMO_QUERIES["multi_collection"])
        print(f"Selected collections: {result_multi.selected_collections}")
        print(result_multi.final_answer)

        print("\n3) Follow-up question")
        history = [
            ChatMessage(role="assistant", content=result_multi.final_answer),
        ]
        result_follow_up = assistant.ask_follow_up(history, DEMO_QUERIES["follow_up"])
        print(f"Selected collections: {result_follow_up.selected_collections}")
        print(result_follow_up.final_answer)

        print("\n4) Filtering / aggregation logic")
        result_filter = assistant.ask_with_english_courses_filter(
            DEMO_QUERIES["filter_or_aggregation"]
        )
        print(f"Selected collections: {result_filter.selected_collections}")
        print(result_filter.final_answer)

        print("\n5) Free-form query")
        result_free = assistant.ask(DEMO_QUERIES["free_form"])
        print(f"Selected collections: {result_free.selected_collections}")
        print(result_free.final_answer)

        print("\n=== Demo complete ===")
    finally:
        assistant.close()


if __name__ == "__main__":
    run_demo()
