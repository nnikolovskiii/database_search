import streamlit as st
import time
from app.chains.create_sql_query_chain import create_sql_query

st.set_page_config(page_title="Ask SQL generator", page_icon="random", layout="centered")
st.header("Ask SQL generator :loudspeaker:")
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
        time.sleep(2)
        response = create_sql_query(prompt)
    except Exception as e:
        response = f"An error occurred: {e}"

    st.session_state.chat_history[-1]["response"] = response

    typing_indicator.empty()

    st.markdown(
        f'<div class="chat-container"><div class="chat-bubble bot-bubble">{response}</div></div>',
        unsafe_allow_html=True)
