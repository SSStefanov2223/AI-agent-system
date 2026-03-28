import streamlit as st
from weaviate.agents.classes import ChatMessage

from demo_queries import DEMO_QUERY_ITEMS
from personalization_agent import (
    UniversityPersonalizationExtension,
    format_personalization_result,
)
from personalization_profiles import PERSONA_OPTION_LABELS
from query_agent import UniversityQueryAssistant, format_search_response


st.set_page_config(page_title="University Query Agent", page_icon="🎓", layout="wide")

def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_query" not in st.session_state:
        st.session_state.input_query = ""


@st.cache_resource
def get_assistant() -> UniversityQueryAssistant:
    return UniversityQueryAssistant()


@st.cache_resource
def get_personalization_extension() -> UniversityPersonalizationExtension:
    return UniversityPersonalizationExtension()


def set_query(text: str) -> None:
    st.session_state.input_query = text


def render_chat(messages: list[dict]) -> None:
    for message in messages:
        role = message.get("role", "assistant")
        with st.chat_message(role):
            st.markdown(message.get("content", ""))
            selected = message.get("selected_collections")
            if selected:
                st.caption(f"Collections: {', '.join(selected)}")


def build_chat_history_for_agent(messages: list[dict]) -> list[ChatMessage]:
    history: list[ChatMessage] = []
    for message in messages:
        role = message.get("role")
        content = message.get("content", "")
        if role in {"user", "assistant"} and content:
            history.append(ChatMessage(role=role, content=content))
    return history


def main() -> None:
    init_state()
    st.title("🎓 University Query Agent")
    st.write("Natural language assistant over Weaviate collections: Courses + Instructors.")

    with st.sidebar:
        st.subheader("Mode")
        mode = st.radio(
            "Choose query mode",
            options=[
                "Ask",
                "Search",
                "Ask (English courses filter)",
                "Personalized Recommendations",
            ],
            index=0,
        )

        selected_profile_id = None
        if mode == "Personalized Recommendations":
            selected_profile_id = st.selectbox(
                "Persona profile",
                options=list(PERSONA_OPTION_LABELS.keys()),
                format_func=lambda key: PERSONA_OPTION_LABELS[key],
            )

        st.subheader("Demo queries")
        for label, text in DEMO_QUERY_ITEMS:
            st.button(label, use_container_width=True, on_click=set_query, args=(text,))

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    render_chat(st.session_state.messages)

    query = st.chat_input("Ask about courses, instructors, ECTS, skills...", key="input_query")

    if not query:
        return

    assistant = get_assistant()

    user_message = {"role": "user", "content": query}
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Query Agent is thinking..."):
            if mode == "Search":
                search_response, selected = assistant.search(query, limit=5)
                answer = format_search_response(search_response)
                payload = {
                    "role": "assistant",
                    "content": answer,
                    "selected_collections": selected,
                }
            elif mode == "Ask (English courses filter)":
                result = assistant.ask_with_english_courses_filter(query)
                payload = {
                    "role": "assistant",
                    "content": result.final_answer,
                    "selected_collections": result.selected_collections,
                }
            elif mode == "Personalized Recommendations":
                personalization_extension = get_personalization_extension()
                result = personalization_extension.recommend(
                    profile_id=selected_profile_id,
                    limit=5,
                    instruction=query,
                    use_agent_ranking=True,
                )
                payload = {
                    "role": "assistant",
                    "content": format_personalization_result(result),
                    "selected_collections": ["Courses (Personalization Agent)"],
                }
            else:
                if st.session_state.messages[:-1]:
                    history = build_chat_history_for_agent(st.session_state.messages[:-1])
                    history.append(ChatMessage(role="user", content=query))
                    result = assistant.ask_conversation(history)
                else:
                    result = assistant.ask(query)

                payload = {
                    "role": "assistant",
                    "content": result.final_answer,
                    "selected_collections": result.selected_collections,
                }

        st.markdown(payload["content"])
        st.caption(f"Collections: {', '.join(payload['selected_collections'])}")

    st.session_state.messages.append(payload)


if __name__ == "__main__":
    main()
