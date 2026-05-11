import streamlit as st
import ollama

# Page config
st.set_page_config(
    page_title="Fides - Catholic AI Companion",
    page_icon="✝️",
    layout="centered"
)

# Header
st.title("✝️ Fides")
st.caption("Your faithful Catholic AI companion")

# System prompt
system_prompt = """You are Fides, a faithful and trustworthy Catholic AI companion. 
You help Catholics with questions about their faith, Church teaching, scripture, 
saints, and prayer. Always ground your answers in Catholic tradition and teaching. 
Be warm, clear, and pastoral in tone. When relevant, cite the Catechism of the 
Catholic Church or scripture. Always remind users to consult their priest for 
matters of conscience or spiritual direction."""

# Disclaimer
st.info("🙏 Fides is a faith companion, not a substitute for your priest or spiritual director.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the faith..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Fides response
    with st.chat_message("assistant"):
        with st.spinner("Fides is reflecting..."):
            response = ollama.chat(
                model="gemma3",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ]
            )
            reply = response['message']['content']
            st.markdown(reply)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": reply}) 
