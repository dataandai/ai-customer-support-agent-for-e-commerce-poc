import streamlit as st
import requests

st.set_page_config(page_title="TechMart AI Support", page_icon="🤖")
st.title("🛒 TechMart Customer Support")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Assuming main.py is running on localhost:8000
            response = requests.post(
                "http://localhost:8000/chat", 
                json={"message": prompt, "history": []}
            )
            if response.status_code == 200:
                answer = response.json()["reply"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Backend error. Ensure main.py is running.")
        except Exception as e:
            st.error(f"Connection failed: {e}")