import streamlit as st
import requests
from app.databases.postgres_database.database_connection import get_all_registered_databases

st.set_page_config(page_title="Ask SQL generator", page_icon="random", layout="centered")

col1, col2 = st.columns([3, 2])

with col1:
    st.header("Ask SQL generator :loudspeaker:")

with col2:
    def fetch_database_names():
        return get_all_registered_databases()


    databases = fetch_database_names()
    selected_database = st.selectbox("Select DB", databases)

st.markdown("<hr style='margin-top: 0'>", unsafe_allow_html=True)

bubble_css = """
          <style>
          .chat-bubble {
              padding: 10px;
              border-radius: 15px;
              margin: 10px;
              max-width: 80%;
              display: inline-block;
          }
          .user-bubble {
              text-align: right;
              align-self: flex-end;
              border-bottom-right-radius: 0;
              margin-right: 0px;
              background-color: #33383D;
              color: white;
          }
          .bot-bubble {
              align-self: flex-start;
              text-align: left;
              border-bottom-left-radius: 0;
              background-color: #284150;
              color: white;
          }
          .chat-container {
               display: flex;
               flex-direction: column;
          }
          </style>
          """

st.markdown(bubble_css, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(
            f'<div class="chat-container"><div class="chat-bubble user-bubble">{chat["question"]}</div></div>',
            unsafe_allow_html=True)
        st.markdown(
            f'<div class="chat-container"><div class="chat-bubble bot-bubble">{chat["response"]}</div></div>',
            unsafe_allow_html=True)

prompt = st.chat_input("What would you like to ask?")

if prompt:
    st.session_state.chat_history.append({"question": prompt, "response": "..."})
    st.markdown(
        f'<div class="chat-container"><div class="chat-bubble user-bubble">{prompt}</div></div>',
        unsafe_allow_html=True)

    typing_indicator = st.empty()
    typing_indicator.markdown(
        f'<div class="chat-container"><div class="chat-bubble bot-bubble">...</div></div>',
        unsafe_allow_html=True
    )

    try:
        url = f"http://localhost:8000/chat/{selected_database}?prompt={prompt}"
        response = requests.post(url)
        if response.status_code == 200:
            response_data = response.json()
            query = response_data.get("query", "No query generated")
        else:
            query = f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        query = f"An error occurred: {e}"

    st.session_state.chat_history[-1]["response"] = query

    typing_indicator.empty()

    st.markdown(
        f'<div class="chat-container"><div class="chat-bubble bot-bubble">{query}</div></div>',
        unsafe_allow_html=True)
