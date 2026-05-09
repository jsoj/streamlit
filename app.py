
import streamlit as st
import requests
import json

st.set_page_config(page_title="Gemma 4 Chat", page_icon="🤖")

st.title("🤖 Gemma 4 na minha VPS")

# Configuração do Ollama (O Coolify usa o nome do serviço como host na rede Docker)
# Se o Ollama e o Streamlit estiverem no mesmo servidor Coolify, 
# use o endereço IP interno ou o nome do serviço.
OLLAMA_URL = st.sidebar.text_input("Ollama Endpoint", "http://localhost:11434/api/generate")
MODEL_NAME = st.sidebar.text_input("Modelo", "gemma4:26b")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para o Gemma 4 via Ollama
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True
            }
            
            response = requests.post(OLLAMA_URL, json=payload, stream=True)
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    text = chunk.get("response", "")
                    full_response += text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro ao conectar com o Gemma 4: {e}")
