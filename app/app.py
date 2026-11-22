
import sys
from pathlib import Path

import streamlit as st

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pdf_processor import extract_text_from_pdf
from src.text_splitter import split_text_into_chunks
from src.vector_store import create_vector_store, search_similar_chunks
from src.chatbot import generate_answer


# Page configuration
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI-Powered PDF Chatbot")
st.write("Upload a PDF and ask questions about its contents.")

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# PDF upload
uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file:
    st.info(f"Selected file: {uploaded_file.name}")

    if st.button("Process PDF"):
        try:
            with st.spinner("Reading and processing your PDF..."):

                pages = extract_text_from_pdf(uploaded_file)

                chunks = split_text_into_chunks(pages)

                embeddings, stored_chunks, model = (
                    create_vector_store(chunks)
                )

                st.session_state.embeddings = embeddings
                st.session_state.chunks = stored_chunks
                st.session_state.embedding_model = model
                st.session_state.processed = True
                st.session_state.chat_history = []

            st.success(
                f"PDF processed successfully! "
                f"{len(pages)} pages and {len(chunks)} text chunks."
            )

        except Exception as error:
            st.error(f"PDF processing failed: {error}")


# Chat section
if st.session_state.processed:

    st.subheader("Ask questions about your PDF")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about your PDF...")

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching your PDF and generating an answer..."):

                    relevant_chunks = search_similar_chunks(
                        question,
                        st.session_state.embeddings,
                        st.session_state.chunks,
                        st.session_state.embedding_model,
                        top_k=5
                    )

                    answer = generate_answer(
                        question,
                        relevant_chunks
                    )

                st.markdown(answer)

                pages_found = sorted({
                    chunk["page"] for chunk in relevant_chunks
                })

                st.caption(
                    "Relevant PDF pages: "
                    + ", ".join(map(str, pages_found))
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"Unable to generate answer: {error}")

else:
    st.info("Upload and process a PDF to start chatting.")
