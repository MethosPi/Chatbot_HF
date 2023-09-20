import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os

# Titolo dell'app
st.set_page_config(page_title="DP Chatbot")
login_email = st.secrets['EMAIL']
login_pass = st.secrets['PASS']

st.title('AIChat by DeltaPi')
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm DeltaPi. How can I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm DeltaPi. How can I help you?"}]

st.sidebar.title('AIChat by DeltaPi')
st.sidebar.button('Clear Chat', on_click=clear_chat_history)

def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "I'm here to help you."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.chat(prompt)

if prompt := st.chat_input(disabled=not (login_email and login_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Processing.."):
            response = generate_response(prompt, login_email, login_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
