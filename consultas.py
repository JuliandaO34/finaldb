import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

# Función para obtener todas las asistencias
def mostrar_asistencias():
    response = requests.get(f"{BASE_URL}/asistencias/")
    if response.status_code == 200:
        asistencias = response.json()
        df_asistencias = pd.DataFrame(asistencias)
        st.dataframe(df_asistencias)
    else:
        st.error("Error al recuperar las asistencias.")

# Función para obtener todos los actores
def mostrar_actores():
    response = requests.get(f"{BASE_URL}/actores/")
    if response.status_code == 200:
        actores = response.json()
        df_actores = pd.DataFrame(actores)
        st.dataframe(df_actores)
    else:
        st.error("Error al recuperar los actores.")

# Función para obtener todos los teatros
def mostrar_teatros():
    response = requests.get(f"{BASE_URL}/teatros/")
    if response.status_code == 200:
        teatros = response.json()
        df_teatros = pd.DataFrame(teatros)
        st.dataframe(df_teatros)
    else:
        st.error("Error al recuperar los teatros.")

# Función para obtener todas las funciones
def mostrar_funciones():
    response = requests.get(f"{BASE_URL}/funciones/")
    if response.status_code == 200:
        funciones = response.json()
        df_funciones = pd.DataFrame(funciones)
        st.dataframe(df_funciones)
    else:
        st.error("Error al recuperar las funciones.")

# Función para obtener todos los roles
def mostrar_roles():
    response = requests.get(f"{BASE_URL}/roles/")
    if response.status_code == 200:
        roles = response.json()
        df_roles = pd.DataFrame(roles)
        st.dataframe(df_roles)
    else:
        st.error("Error al recuperar los roles.")

# Función para obtener todas las entradas
def mostrar_entradas():
    response = requests.get(f"{BASE_URL}/entradas/")
    if response.status_code == 200:
        entradas = response.json()
        df_entradas = pd.DataFrame(entradas)
        st.dataframe(df_entradas)
    else:
        st.error("Error al recuperar las entradas.")

# Función para obtener la entrada máxima
def max_entrada():
    response = requests.get(f"{BASE_URL}/entradas/max/")
    if response.status_code == 200:
        max_total = response.json()
        st.write("Entrada máxima:", max_total["max_total"])
    else:
        st.error("Error al recuperar la entrada máxima.")

# Función para obtener la entrada mínima
def min_entrada():
    response = requests.get(f"{BASE_URL}/entradas/min/")
    if response.status_code == 200:
        min_total = response.json()
        st.write("Entrada mínima:", min_total["min_total"])
    else:
        st.error("Error al recuperar la entrada mínima.")

# Función para obtener el promedio de entradas
def avg_entrada():
    response = requests.get(f"{BASE_URL}/entradas/avg/")
    if response.status_code == 200:
        avg_total = response.json()
        st.write("Promedio de entradas:", avg_total["avg_total"])
    else:
        st.error("Error al recuperar el promedio de entradas.")

# Ejemplo de consulta adicional
def consultar_funciones_asistencias():
    response = requests.get(f"{BASE_URL}/consultas/")
    if response.status_code == 200:
        datos = response.json()
        df = pd.DataFrame(datos, columns=["titulo", "actor_nombre", "rol_nombre"])
        st.dataframe(df)
    else:
        st.error("Error al recuperar las funciones con asistencias.")

# Agrega más consultas según sea necesario
def consultar_funciones_por_teatro(teatro_id):
    response = requests.get(f"{BASE_URL}/funciones/")  # Modificar según API
    if response.status_code == 200:
        funciones = response.json()  # Filtrar por teatro_id si es necesario
        df_funciones = pd.DataFrame(funciones)
        st.dataframe(df_funciones)
    else:
        st.error("Error al recuperar las funciones por teatro.")
