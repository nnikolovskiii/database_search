import streamlit as st

from app.chains.create_sql_query_chain import create_sql_query


def main():
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
          }
          .bot-bubble {
              align-self: flex-start;
              text-align: left;
              border-bottom-left-radius: 0;
              background-color: #284150;

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
        st.session_state.chat_history.append({"question": prompt, "response": ""})
        st.markdown(
            f'<div class="chat-container"><div class="chat-bubble user-bubble">{prompt}</div></div>',
            unsafe_allow_html=True)

        try:
            response = create_sql_query(prompt)
        except Exception as e:
            response = f"An error occurred: {e}"

        st.markdown(
            f'<div class="chat-container"><div class="chat-bubble bot-bubble">{response}</div></div>',
            unsafe_allow_html=True)


if __name__ == "__main__":
    main()
