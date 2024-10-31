import streamlit as st
import requests

st.title("Gestión de Teatro")

# Insertar un nuevo actor
st.header("Agregar Actor")
nombre = st.text_input("Nombre")
fecha_nacimiento = st.date_input("Fecha de Nacimiento")
nacionalidad = st.text_input("Nacionalidad")
if st.button("Agregar Actor"):
    response = requests.post("http://127.0.0.1:8000/actores/", json={"nombre": nombre, "fecha_nacimiento": str(fecha_nacimiento), "nacionalidad": nacionalidad})
    st.success(response.json()["message"])

# Consultar actores
st.header("Lista de Actores")
if st.button("Ver Actores"):
    response = requests.get("http://127.0.0.1:8000/actores/")
    for actor in response.json():
        st.write(actor)

# Repetir para teatros, funciones, entradas y asistencias...
<<<<<<< Updated upstream

# Consultar actores
st.header("Lista de Actores")
if st.button("Ver Actores"):
    response = requests.get("http://127.0.0.1:8000/actores/")
    for actor in response.json():
        st.write(actor)
=======
>>>>>>> Stashed changes
