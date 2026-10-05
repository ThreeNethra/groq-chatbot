# Groq Chatbot

A simple chatbot made with Streamlit, LangChain and Groq (`openai/gpt-oss-120b`). It keeps the chat history in the session and streams the answers.

This repo is used for Assignment 39 (deploying a GenAI app on Streamlit Cloud and Hugging Face Spaces).

## Run locally

```
pip install -r requirements.txt
set GROQ_API_KEY=your_key
streamlit run app.py
```

The app needs a Groq API key in the `GROQ_API_KEY` secret / environment variable. The key is not stored in the code.
