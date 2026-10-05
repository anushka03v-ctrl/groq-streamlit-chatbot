import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY nahi mili. .env file check karo.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Groq AI Chatbot")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:

    # User message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        with st.chat_message("assistant"):

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Give clear and simple answers."
                    },
                    *st.session_state.messages
                ]
            )

            answer = response.choices[0].message.content

            st.write(answer)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Error: {e}")
