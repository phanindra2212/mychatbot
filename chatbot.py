from openai import OpenAI
import streamlit as st

st.title("AI Chatbot")

# Sidebar
api_key = st.sidebar.text_input(
    "Enter OpenRouter API Key",
    type="password"
)

model_name = st.sidebar.text_input(
    "Enter Model Name",
    value="openai/gpt-oss-120b:free"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask anything...")

if user_input:

    if not api_key:
        st.error("Please enter your OpenRouter API Key.")
        st.stop()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model=model_name,
        messages=st.session_state.messages
    )

    assistant_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    with st.chat_message("assistant"):
        st.write(assistant_reply)
