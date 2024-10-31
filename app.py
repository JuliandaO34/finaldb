import streamlit as st
import pandas as pd
import requests

# Función para cargar y procesar el archivo Excel
def cargar_excel():
    st.header("Cargar archivo de Excel")
    uploaded_file = st.file_uploader("Elige un archivo de Excel", type="xlsx")
    
    if uploaded_file is not None:
        # Leer el archivo Excel
        excel_file = pd.ExcelFile(uploaded_file)
        hojas = excel_file.sheet_names
        
        st.write("Hojas disponibles:", hojas)
        
        for hoja in hojas:
            st.write(f"Datos de la hoja: {hoja}")
            df = pd.read_excel(uploaded_file, sheet_name=hoja)
            st.write(df)
            
            if st.button(f"Insertar datos de {hoja} en la base de datos"):
                # Aquí puedes enviar los datos a tu API
                for _, row in df.iterrows():
                    # Lógica de inserción basada en el nombre de la hoja
                    if hoja == "actores":
                        response = requests.post("http://127.0.0.1:8000/actores/", json=row.to_dict())
                    elif hoja == "funciones":
                        response = requests.post("http://127.0.0.1:8000/funciones/", json=row.to_dict())
                    elif hoja == "entradas":
                        response = requests.post("http://127.0.0.1:8000/entradas/", json=row.to_dict())
                    elif hoja == "asistencias":
                        response = requests.post("http://127.0.0.1:8000/asistencias/", json=row.to_dict())
                    # Añadir más casos según sea necesario
                    
                st.success(f"Datos de {hoja} insertados exitosamente.")

# Función para insertar un actor
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

# Función para insertar una función
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

# Función para insertar una entrada
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

# Función para mostrar funciones
def mostrar_funciones():
    st.header("Funciones Disponibles")
    response = requests.get("http://127.0.0.1:8000/funciones/")
    if response.status_code == 200:
        funciones = response.json()
        st.write(funciones)
    else:
        st.error("Error al recuperar las funciones.")

# Función para mostrar asistencias
def mostrar_asistencias():
    st.header("Asistencias Disponibles")
    response = requests.get("http://127.0.0.1:8000/asistencias/")
    if response.status_code == 200:
        asistencias = response.json()
        st.write(asistencias)
    else:
        st.error("Error al recuperar las asistencias.")

# Función principal de la aplicación
def main():
    st.sidebar.title("Navegación")
    options = st.sidebar.radio("Selecciona una tabla", ("Inicio", "Actores", "Funciones", "Entradas", "Asistencias"))

    if options == "Inicio":
        st.title("Gestión de Teatro")
        st.write("Bienvenido a la gestión de teatro. Selecciona una opción en la barra lateral para comenzar.")
        cargar_excel()  # Llamar a la función para cargar el archivo de Excel
    
    elif options == "Actores":
        insertar_actor()

    elif options == "Funciones":
        insertar_funcion()
        mostrar_funciones()

    elif options == "Entradas":
        insertar_entrada()

    elif options == "Asistencias":
        mostrar_asistencias()

if __name__ == "__main__":
    main()
