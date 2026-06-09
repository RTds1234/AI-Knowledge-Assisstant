import streamlit as st

from utils.helper import (
    process_files,
    ask_question
)

st.set_page_config(
    page_title="AI Knowledge Assistant",
    layout="wide"
)

st.title(
    "📚 AI Knowledge Assistant"
)

if "messages" not in st.session_state:

    st.session_state.messages = []


with st.sidebar:

    st.header("Upload Files")

    uploaded_files = st.file_uploader(
        "Choose files",
        type=[
            "pdf",
            "txt",
            "docx",
            "csv",
            "md"
        ],
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button(
            "Process Files"
        ):

            with st.spinner(
                "Processing..."
            ):

                chunks = process_files(
                    uploaded_files
                )

            st.success(
                f"{chunks} chunks added"
            )

    st.divider()

    if st.button(
        "Clear Chat"
    ):

        st.session_state.messages = []

        st.rerun()


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if (
            msg["role"] == "assistant"
            and "sources" in msg
        ):

            st.markdown("### Sources")

            for source in msg["sources"]:
                st.markdown(f"- {source}")


question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    answer, sources, rewritten_question = ask_question(
    question,
    st.session_state.messages
    )

    source_text = "\n\n### Sources\n"

    for source in sources:

        source_text += (
            f"- {source}\n"
        )

    final_answer = (
        answer +
        source_text
    )

    st.session_state.messages.append(
    {
        "role": "assistant",
        "content": answer,
        "sources": sources
    }
    )

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            final_answer
        )