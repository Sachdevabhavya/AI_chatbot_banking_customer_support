import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from chatbot import get_response

# Set up the Streamlit page
st.set_page_config(page_title="Banking Chatbot", layout="wide")

# Add a page title
st.title("Banking Customer Service Chatbot")

# Custom styling
st.markdown("""
    <style>
    .chat-container {
        max-width: 700px;
        margin: auto;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 80%;
        display: inline-block;
    }
    .user-bubble {
        background-color: #EAEAEA;
        text-align: left;
        align-self: flex-start;
    }
    .bot-bubble {
        background-color: #DCF8C6;
        text-align: right;
        align-self: flex-end;
    }
    .scrollable-chat {
        max-height: 500px;
        overflow-y: auto;
        padding-bottom: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat Display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="scrollable-chat">', unsafe_allow_html=True)

for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-bubble user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close chat div
st.markdown('</div>', unsafe_allow_html=True)  # Close container div

# Fixed input box
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):  # Ensure form clears on submit
        user_input = st.text_input("Type your message:", key="user_input")
        submit_button = st.form_submit_button("Send")

# Handle user input
if submit_button and user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Get chatbot response
    bot_response = get_response(user_input)

    # Add bot response to chat history
    st.session_state["messages"].append({"role": "bot", "content": bot_response})
