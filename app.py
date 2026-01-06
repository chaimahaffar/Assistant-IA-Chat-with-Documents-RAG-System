import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="RAG system", layout="centered")

st.title("💬 Assistant IA : Chat with Documents")
st.write("Ask questions based on your documents")

# Mémoire du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l’historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input utilisateur
user_input = st.chat_input("Type your question here...")

if user_input:
    # afficher message utilisateur
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # appel API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                json={"question": user_input}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = "Error calling the RAG API"

            st.markdown(answer)

    # sauvegarde réponse
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
