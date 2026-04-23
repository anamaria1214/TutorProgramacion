import streamlit as st
from script import tutor_grafo
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Tutor IA", page_icon="🎓")
st.title("🎓 Mi Tutor de Programación")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)

if st.sidebar.button("Limpiar historial"):
    st.session_state.chat_history = []
    st.rerun()

if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        config = {"configurable": {"thread_id": "usuario_streamlit_1"}}
        
        historial_reducido = st.session_state.chat_history[-3:]

        respuesta_grafo = tutor_grafo.invoke(
            {"messages": historial_reducido}, 
            config
        )
        
        contenido_ia = respuesta_grafo["messages"][-1].content
        st.markdown(contenido_ia)
        
        st.session_state.chat_history.append(AIMessage(content=contenido_ia))