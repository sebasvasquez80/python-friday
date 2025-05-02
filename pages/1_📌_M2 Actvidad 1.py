import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Momento 2 - Actividad 1")

st.header("Descripción de la actividad")
st.markdown("""
Esta actividad es una introducción práctica a Python y a las estructuras de datos básicas.
En ella, exploraremos los conceptos fundamentales de Python y aprenderemos a utilizar variables,
tipos de datos, operadores, y las estructuras de datos más utilizadas como listas, tuplas,
diccionarios y conjuntos.
""")

st.header("Objetivos de aprendizaje")

st.markdown("""
- Comprender los tipos de datos básicos en Python
- Aprender a utilizar variables y operadores
- Dominar las estructuras de datos fundamentales
- Aplicar estos conocimientos en ejemplos prácticos
""")

st.header("Solución actividad 1")

soccer = { "Club" : ["FC Barcelona", "Real Madrid CF", "Atletico Madrid", "Valencia", "Sevilla"],
          "Ganados": ["10","8","6","4","2"],
          "Empatados": ["0","1","2","3","5"],
          "Perdidos": ["0","1","2","3","3"],
          "Puntos":["30","25","20","15","10"],}

table = pd.DataFrame(soccer)
table.index = range(1, len(table) + 1)

st.subheader ("Creación de DataFrame con diccionario")
st.code("""
    soccer = { "Club" : ["FC Barcelona", "Real Madrid CF", "Atletico Madrid", "Valencia", "Sevilla"],
          "Ganados": ["10","8","6","4","2"],
          "Empatados": ["0","1","2","3","5"],
          "Perdidos": ["0","1","2","3","3"],
          "Puntos":["30","25","20","15","10"],}

table = pd.DataFrame(soccer)
table.index = range(1, len(table) + 1)

st.dataframe(table)
""", language='python')

st.subheader ("Tabla de posiciones")
st.dataframe(table)