import os

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

st.set_page_config(page_title="Groq Chatbot")
st.title("Groq Chatbot")
st.caption("A simple chatbot using Groq and LangChain")


def get_api_key():
    # Hugging Face gives secrets as environment variables,
    # Streamlit Cloud gives them through st.secrets (and env variables too)
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            key = st.secrets["GROQ_API_KEY"]
        except Exception:
            key = None
    return key


api_key = get_api_key()
if not api_key:
    st.error("GROQ_API_KEY is not set. Add it in the app secrets (or as an environment variable when running locally).")
    st.stop()

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", ["openai/gpt-oss-120b", "openai/gpt-oss-20b"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    if st.button("Clear chat"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Keep your answers short and clear."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
llm = ChatGroq(model=model, temperature=temperature, api_key=api_key)
chain = prompt | llm | StrOutputParser()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Type your message")

if question:
    with st.chat_message("user"):
        st.write(question)

    history = [("human" if m["role"] == "user" else "ai", m["content"]) for m in st.session_state.messages]

    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(chain.stream({"history": history, "question": question}))
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Could not get a response: {e}")
