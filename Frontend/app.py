import streamlit as st
import pandas as pd
import requests
import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def cargar_excel():
    st.header("Cargar archivo de Excel")
    uploaded_file = st.file_uploader("Elige un archivo de Excel", type="xlsx")
    
    if uploaded_file is not None:
        
        excel_file = pd.ExcelFile(uploaded_file)
        hojas = excel_file.sheet_names
        
        st.write("Hojas disponibles:", hojas)
        
        for hoja in hojas:
            st.write(f"Datos de la hoja: {hoja}")
            df = pd.read_excel(uploaded_file, sheet_name=hoja)
            st.write(df)
            
            if st.button(f"Insertar datos de {hoja} en la base de datos"):
                for _, row in df.iterrows():
                    if hoja == "actores":
                        response = requests.post("http://127.0.0.1:8000/actores/", json=row.to_dict())
                    elif hoja == "teatros":
                        response = requests.post("http://127.0.0.1:8000/teatros/", json=row.to_dict())
                    elif hoja == "funciones":
                        response = requests.post("http://127.0.0.1:8000/funciones/", json=row.to_dict())
                    elif hoja == "roles":
                        response = requests.post("http://127.0.0.1:8000/roles/", json=row.to_dict())
                    elif hoja == "entradas":
                        response = requests.post("http://127.0.0.1:8000/entradas/", json=row.to_dict())
                    elif hoja == "asistencias":
                        response = requests.post("http://127.0.0.1:8000/asistencias/", json=row.to_dict())
                    
                st.success(f"Datos de {hoja} insertados exitosamente.")

def insertar_actor():
    st.header("Insertar Actor")
    nombre = st.text_input("Nombre")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento")
    nacionalidad = st.text_input("Nacionalidad")
    
    if st.button("Agregar Actor"):
        response = requests.post("http://127.0.0.1:8000/actores/", json={
            "nombre": nombre,
            "fecha_nacimiento": str(fecha_nacimiento),
            "nacionalidad": nacionalidad
        })
        if response.status_code == 200:
            st.success("Actor agregado exitosamente.")
        else:
            st.error("Error al agregar el actor.")

def mostrar_actores():
    st.header("Actores Disponibles")
    response = requests.get("http://127.0.0.1:8000/actores/")
    if response.status_code == 200:
        actores = response.json()
        df_actores = pd.DataFrame(actores)
        st.dataframe(df_actores)
    else:
        st.error("Error al recuperar los actores.")


def insertar_teatro():
    st.header("Insertar Teatro")
    nombre = st.text_input("Nombre del Teatro")
    direccion = st.text_input("Dirección")
    ciudad = st.text_input("Ciudad")
    
    if st.button("Agregar Teatro"):
        response = requests.post("http://127.0.0.1:8000/teatros/", json={
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad
        })
        if response.status_code == 200:
            st.success("Teatro agregado exitosamente.")
        else:
            st.error("Error al agregar el teatro.")

def mostrar_teatros():
    st.header("Teatros Disponibles")
    response = requests.get("http://127.0.0.1:8000/teatros/")
    if response.status_code == 200:
        teatros = response.json()
        df_teatros = pd.DataFrame(teatros)
        st.dataframe(df_teatros)
    else:
        st.error("Error al recuperar los teatros.")


def insertar_funcion():
    st.header("Insertar Función")
    titulo = st.text_input("Título")
    fecha = st.date_input("Fecha")
    teatro_id = st.number_input("Teatro ID", min_value=1)
    precio = st.number_input("Precio", min_value=0.0, format="%.2f")
    
    if st.button("Agregar Función"):
        response = requests.post("http://127.0.0.1:8000/funciones/", json={
            "titulo": titulo,
            "fecha": str(fecha),
            "teatro_id": teatro_id,
            "precio": precio
        })
        if response.status_code == 200:
            st.success("Función agregada exitosamente.")
        else:
            st.error("Error al agregar la función.")


def insertar_rol():
    st.header("Insertar Rol")
    nombre = st.text_input("Nombre del Rol")
    
    if st.button("Agregar Rol"):
        response = requests.post("http://127.0.0.1:8000/roles/", json={
            "nombre": nombre
        })
        if response.status_code == 200:
            st.success("Rol agregado exitosamente.")
        else:
            st.error("Error al agregar el rol.")


def mostrar_roles():
    st.header("Roles Disponibles")
    response = requests.get("http://127.0.0.1:8000/roles/")
    if response.status_code == 200:
        roles = response.json()
        df_roles = pd.DataFrame(roles)
        st.dataframe(df_roles)
    else:
        st.error("Error al recuperar los roles.")


def insertar_entrada():
    st.header("Insertar Entrada")
    funcion_id = st.number_input("Función ID", min_value=1)
    fecha_compra = st.date_input("Fecha de Compra")
    cantidad = st.number_input("Cantidad", min_value=1)
    total = st.number_input("Total", min_value=0.0, format="%.2f")
    
    if st.button("Agregar Entrada"):
        response = requests.post("http://127.0.0.1:8000/entradas/", json={
            "funcion_id": funcion_id,
            "fecha_compra": str(fecha_compra),
            "cantidad": cantidad,
            "total": total
        })
        if response.status_code == 200:
            st.success("Entrada agregada exitosamente.")
        else:
            st.error("Error al agregar la entrada.")


def mostrar_funciones():
    st.header("Funciones Disponibles")
    response = requests.get("http://127.0.0.1:8000/funciones/")
    if response.status_code == 200:
        funciones = response.json()
        df_funciones = pd.DataFrame(funciones)
        st.dataframe(df_funciones)
    else:
        st.error("Error al recuperar las funciones.")


def mostrar_asistencias():
    st.header("Asistencias Disponibles")
    response = requests.get("http://127.0.0.1:8000/asistencias/")
    if response.status_code == 200:
        asistencias = response.json()
        df_asistencias = pd.DataFrame(asistencias)
        st.dataframe(df_asistencias)
    else:
        st.error("Error al recuperar las asistencias.")

def recaudacion_teatro():
    st.header("Recaudacion Teatro")
    response = requests.get("http://127.0.0.1:8000/consultas/recaudacion_teatro")
    if response.status_code == 200:
        recaudacion_teatro= response.json()
        df_recaudacion_teatro = pd.DataFrame(recaudacion_teatro)
        st.dataframe(df_recaudacion_teatro)
    else:
        st.error("Error al recuperar las recaudaciones.")

def get_total_asistencia():
    st.header("total asistencia")
    response = requests.get("http://127.0.0.1:8000/consultas/total_asistencia")
    if response.status_code == 200:
        total_asistencia= response.json()
        df_total_asistencia = pd.DataFrame(total_asistencia)
        st.dataframe(df_total_asistencia)
    else:
        st.error("Error al recuperar las asistencias.")

def get_entrada_mas_cara():
    st.header("Entrada mas cara")
    response = requests.get("http://127.0.0.1:8000/consultas/entrada_mas_cara")
    if response.status_code == 200:
        entrada_mas_cara= response.json()
        df_entrada_mas_cara = pd.DataFrame(entrada_mas_cara)
        st.dataframe(df_entrada_mas_cara)
    else:
        st.error("Error al recuperar las entradas.")

def get_entrada_mas_barata():
    st.header("Entrada mas barata")
    response = requests.get("http://127.0.0.1:8000/consultas/entrada_mas_barata")
    if response.status_code == 200:
        entrada_mas_barata= response.json()
        df_entrada_mas_barata = pd.DataFrame(entrada_mas_barata)
        st.dataframe(df_entrada_mas_barata)
    else:
        st.error("Error al recuperar las entradas.")


def get_entradas_funcion():
    st.header("Total entradas funcion")
    response = requests.get("http://127.0.0.1:8000/consultas/total_entradas_funcion")
    if response.status_code == 200:
        total_entradas_funcion= response.json()
        df_total_entradas_funcion = pd.DataFrame(total_entradas_funcion)
        st.dataframe(df_total_entradas_funcion)
    else:
        st.error("Error al recuperar las entradas.")

def get_sin_funcion():
    st.header("Actores sin funcion")
    response = requests.get("http://127.0.0.1:8000/consultas/sin_funcion")
    if response.status_code == 200:
        sin_funcion= response.json()
        df_sin_funcion = pd.DataFrame(sin_funcion)
        st.dataframe(df_sin_funcion)
    else:
        st.error("Error al recuperar las entradas.")

def get_teatros_con_funciones():
    st.header("Teatros con funciones")
    response = requests.get("http://127.0.0.1:8000/consultas/teatros_con_funciones")
    if response.status_code == 200:
        teatro_con_funciones= response.json()
        df_teatro_con_funciones = pd.DataFrame(teatro_con_funciones)
        st.dataframe(df_teatro_con_funciones)
    else:
        st.error("Error al recuperar las entradas.")

def get_funciones_con_entradas():
    st.header("Funciones con entradas")
    response = requests.get("http://127.0.0.1:8000/consultas/funciones_con_entradas")
    if response.status_code == 200:
        funciones_con_entradas= response.json()
        df_funciones_con_entradas = pd.DataFrame(funciones_con_entradas)
        st.dataframe(df_funciones_con_entradas)
    else:
        st.error("Error al recuperar las entradas.")



st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Selecciona una opción", [
    "Cargar Excel",
    "Insertar Actor",
    "Mostrar Actores",
    "Insertar Teatro",
    "Mostrar Teatros",
    "Insertar Función",
    "Insertar Rol",
    "Mostrar Roles",
    "Insertar Entrada",
    "Mostrar Funciones",
    "Mostrar Asistencias",
    "Recaudacion teatro",
    "Total asistencia",
    "Entrada mas cara",
    "Entrada mas barata",
    "Actores sin funcion",
    "Total entradas por funcion",
    "Actores sin funcion",
    "Teatro con funciones",
    "Funciones con entradas "


])


if opcion == "Cargar Excel":
    cargar_excel()
elif opcion == "Insertar Actor":
    insertar_actor()
elif opcion == "Mostrar Actores":
    mostrar_actores()
elif opcion == "Insertar Teatro":
    insertar_teatro()
elif opcion == "Mostrar Teatros":
    mostrar_teatros()
elif opcion == "Insertar Función":
    insertar_funcion()
elif opcion == "Insertar Rol":
    insertar_rol()
elif opcion == "Mostrar Roles":
    mostrar_roles()
elif opcion == "Insertar Entrada":
    insertar_entrada()
elif opcion == "Mostrar Funciones":
    mostrar_funciones()
elif opcion == "Mostrar Asistencias":
    mostrar_asistencias()
elif opcion == "Recaudacion teatro":
    recaudacion_teatro()
elif opcion == "Total asistencia":
    get_total_asistencia()
elif opcion =="Entrada mas cara":
    get_entrada_mas_cara()
elif opcion =="Entrada mas barata":
    get_entrada_mas_barata()
elif opcion == "Total entradas por funcion":
    get_entradas_funcion()
elif opcion == "Actores sin funcion":
    get_sin_funcion()
elif opcion == "Teatro con funciones":
    get_teatros_con_funciones()
elif opcion == "Funciones con entradas":
    get_funciones_con_entradas()
