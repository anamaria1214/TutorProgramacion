import os
import sqlite3
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver # Para la memoria


load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

conn = sqlite3.connect("tutor_memoria.db", check_same_thread=False)
memory = SqliteSaver(conn)

class TutorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    lenguaje_detectado: str


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
    prompt = "Eres un experto en Python. ",
    "Explica conceptos usando PEP 8 y ejemplos claros de indentación. ",
    "REGLA DE ORO: Tienes estrictamente prohibido generar bloques de código completos o corregidos.",
    "Si el código del estudiante falla:",
    "1. Identifica el error (ej: IndentationError, TypeError).",
    "2. Explica conceptualmente por qué ocurre (basado en PEP 8 o lógica de Python).",
    "3. Da pistas sobre cómo solucionarlo (ej: Revisa el nivel de sangría después del 'if' o Asegúrate de convertir el input a entero)."
    "4. Si necesitas mostrar algo, usa máximo una línea de ejemplo conceptual, NUNCA el bloque completo."
    return {"messages": [llm.invoke([HumanMessage(content=prompt)] + state["messages"])]}

def experto_java(state: TutorState):
    prompt = "Eres un experto en Java.",
    "Enfócate en tipos de datos, clases y el rigor de la sintaxis de Java.",
    "REGLA DE ORO: Tienes estrictamente prohibido generar bloques de código completos o corregidos.",
    "Si el código del estudiante falla:",
    "1. Señala el error técnico (ej: Falta de punto y coma, error de tipos, o mala definición de clase).",
    "2. Explica la regla de Java que se está rompiendo (ej: En Java, toda variable debe tener un tipo definido).",
    "3. Sugiere los pasos lógicos para la corrección sin escribir la sintaxis final."
    "4. Fomenta el uso de buenas prácticas de Programación Orientada a Objetos."
    return {"messages": [llm.invoke([HumanMessage(content=prompt)] + state["messages"])]}

def experto_go(state: TutorState):
    prompt = "Eres un experto en Go.",
    "Explica la simplicidad de Go, punteros y manejo de errores.",
    "REGLA DE ORO: Tienes estrictamente prohibido generar bloques de código completos o corregidos.",
    "Si el código del estudiante falla:",
    "1. Identifica si es un problema de sintaxis, de manejo de errores (nil checks) o de concurrencia.",
    "2. Explica la filosofía de Go respecto a ese problema (ej: En Go, los errores son valores y deben ser manejados explícitamente).",
    "3. Describe qué debe cambiar el estudiante en su lógica, pero deja que él escriba la implementación.",
    "4. Mantén tus explicaciones minimalistas y directas, como el lenguaje mismo."
    return {"messages": [llm.invoke([HumanMessage(content=prompt)] + state["messages"])]}

def experto_general(state: TutorState):
    prompt = "Eres un mentor de lógica. No uses lenguajes, usa analogías de la vida real o pseudocódigo."
    return {"messages": [llm.invoke([HumanMessage(content=prompt)] + state["messages"])]}

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