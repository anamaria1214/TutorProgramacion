import streamlit as st
from script import tutor_grafo
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Tutor IA", page_icon="🎓")
st.title("🎓 Mi Tutor de Programación")

# Inicializamos la memoria de la sesión de Streamlit (Interfaz)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostramos los mensajes guardados en la pantalla
for msg in st.session_state.chat_history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

# Input del estudiante
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # 1. Guardar y mostrar mensaje del usuario
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Llamar al Grafo de LangGraph que importamos de script.py
    with st.chat_message("assistant"):
        # Usamos un thread_id único para la sesión del navegador
        config = {"configurable": {"thread_id": "usuario_streamlit_1"}}
        
        # Invocamos el grafo
        respuesta_grafo = tutor_grafo.invoke(
            {"messages": st.session_state.chat_history}, 
            config
        )
        
        # Extraemos el último mensaje de la IA
        contenido_ia = respuesta_grafo["messages"][-1].content
        st.markdown(contenido_ia)
        
        # Guardamos en el historial de la sesión
        st.session_state.chat_history.append(AIMessage(content=contenido_ia))