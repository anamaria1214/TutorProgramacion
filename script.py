import os
import sqlite3
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver # Para la memoria


load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=1024)

conn = sqlite3.connect("tutor_memoria.db", check_same_thread=False)
memory = SqliteSaver(conn)

class TutorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    lenguaje_detectado: str

def prompt_clasificador(lenguaje: str):
    return f"""Eres tutor de {lenguaje} para principiantes. Sé amigable y usa analogías simples.

**EXPLICACIÓN:** Si preguntan "¿qué es?" o "cómo funciona":
- Analogía de la vida real (máx 2 párrafos)
- 1 párrafo técnico  
- Ejemplo pequeño en {lenguaje}

**CÓDIGO:** Si piden "hazme", "código para", "ejercicio":
1. Párrafo explicando qué hace (máx 2 líneas)
2. Código comentado con NÚMEROS DE LÍNEA
3. PRUEBA DE ESCRITORIO en FORMATO LISTA (ver instrucciones abajo)

**INSTRUCCIONES PARA PRUEBA DE ESCRITORIO:**
- SELECCIONA entrada SIMPLE: número 2, string "a", lista pequeña
- NUNCA uses números grandes (23, 100, etc.)
- FORMATO OBLIGATORIO con viñetas y sub-viñetas:
  - **Ejecución con entrada:** [valor concreto]
  - **Línea X:** [descripción del código]
    - Variable: valor
    - Condición: resultado
  - Para bucles: MOSTRAR SOLO resultado comprimido
    - "Bucle ejecuta 3 iteraciones"
    - "Estado final: suma = 6"
  - **Output:** [resultado final]
  - MÁXIMO 10 líneas

Ejemplo modelo:
\`\`\`
**Ejecución con entrada: numero = 2**

**Línea 1:** if (numero < 2)
  - numero: 2, Condición: False

**Línea 2:** for i in range(2, 2)
  - Rango vacío → bucle NO se ejecuta

**Línea 3:** return True

**Output:** True
\`\`\`
"""

def clasificador_nodo(state: TutorState):
    ultimo_mensaje = state["messages"][-1].content
    
    prompt = f"""
    Analiza la duda: "{ultimo_mensaje}"
    Responde UNICAMENTE con una palabra de estas opciones: [python, java, go, general].
    No uses puntos, ni mayúsculas, ni frases adicionales.
    """
    
    respuesta = llm.invoke(prompt)

    lenguaje = respuesta.content.strip().lower().replace(".", "")
    
    opciones_validas = ["python", "java", "go", "general"]
    if lenguaje not in opciones_validas:
        print(f"La IA respondió algo raro: '{lenguaje}'. Redirigiendo a 'general'.")
        lenguaje = "general"
    
    return {"lenguaje_detectado": lenguaje}

def experto_python(state: TutorState):
    prompt = prompt_clasificador("Python")
    mensajes_finales = [SystemMessage(content=prompt)] + state["messages"]
    respuesta = llm.invoke(mensajes_finales)
    return {"messages": [respuesta]}

def experto_java(state: TutorState):
    prompt = prompt_clasificador("Java")
    mensajes_finales = [SystemMessage(content=prompt)] + state["messages"]
    respuesta = llm.invoke(mensajes_finales)
    return {"messages": [respuesta]}


def experto_go(state: TutorState):
    prompt = prompt_clasificador("Go")
    mensajes_finales = [SystemMessage(content=prompt)] + state["messages"]
    respuesta = llm.invoke(mensajes_finales)
    return {"messages": [respuesta]}

def experto_general(state: TutorState):
    prompt = """Eres un mentor de lógica y programación. 
Tu objetivo es explicar conceptos sin usar un lenguaje específico. Usa:
- Analogías de la vida real
- Pseudocódigo o diagramas de flujo descritos
- Ejemplos simples y claros
Mantén un tono amigable y accesible para principiantes."""
    
    mensajes_finales = [SystemMessage(content=prompt)] + state["messages"]
    respuesta = llm.invoke(mensajes_finales)
    return {"messages": [respuesta]}

builder = StateGraph(TutorState)
builder.add_node("clasificador", clasificador_nodo)
builder.add_node("tutor_python", experto_python)
builder.add_node("tutor_java", experto_java)
builder.add_node("tutor_go", experto_go)
builder.add_node("tutor_general", experto_general)

builder.set_entry_point("clasificador")

builder.add_conditional_edges(
    "clasificador",
    lambda state: state["lenguaje_detectado"],
    {"python": "tutor_python", "java": "tutor_java", "go": "tutor_go", "general": "tutor_general"}
)

for node in ["tutor_python", "tutor_java", "tutor_go", "tutor_general"]:
    builder.add_edge(node, END)

tutor_grafo = builder.compile(checkpointer=memory)


def iniciar_tutoría():
    print("--- BIENVENIDO AL TUTOR DE PROGRAMACIÓN IA ---")
    print("Escribe 'salir' para terminar la sesión.\n")
    
    config = {"configurable": {"thread_id": "estudiante_1"}}

    while True:
        entrada_usuario = input("Estudiante: ")
        
        if entrada_usuario.lower() in ["salir", "exit", "quit"]:
            print("¡Suerte con tu código! Vuelve pronto.")
            break

        # Ejecutamos el agente
        eventos = tutor_grafo.stream(
            {"messages": [HumanMessage(content=entrada_usuario)]},
            config,
            stream_mode="values"
        )
        
        # Obtenemos la última respuesta generada en el flujo
        for evento in eventos:
            final_message = evento["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            print(f"\nTutor ({evento['lenguaje_detectado'].upper()}): {final_message.content}\n")

if __name__ == "__main__":
    try:
        iniciar_tutoría()
    finally:
        conn.close()