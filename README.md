# Sistema de Gestión Teatral  
**FastAPI + MySQL + Streamlit**

Este proyecto es un sistema completo para la gestión de actores, funciones, teatros, entradas, roles y asistencias.  
Integra una API construida con **FastAPI**, una base de datos **MySQL**, y una interfaz interactiva desarrollada con **Streamlit**.

Permite:

- Operaciones CRUD completas  
- Carga masiva de datos desde Excel  
- Visualización de tablas  
- Consultas avanzadas (JOIN, MAX, MIN, AVG)  
- Manejo de base de datos relacional  
- API REST estandarizada

---

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI**
- **Streamlit**
- **MySQL**
- **Pydantic**
- **Requests**
- **dotenv**
- **Pandas**

---

## Estructura del proyecto

│── main.py # Backend FastAPI
│── db_connection.py # Conexión a MySQL con variables de entorno
│── app.py # Interfaz Streamlit
│── actors.sql # Script SQL (tablas y base de datos)
│── test_mysql.py # Test de conexión
│── .env # Variables de entorno
│── requirements.txt
│── README.md


---

## 🗄️ Base de datos (MySQL)

El proyecto utiliza una base de datos relacional con las siguientes tablas:

- **actores**
- **teatros**
- **funciones**
- **roles**
- **entradas**
- **asistencias**

El script completo está en:  
`actors.sql`

Incluye relaciones entre tablas, llaves foráneas, y restricciones.

--

Crear entorno virtual

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instalar dependencias

pip install -r requirements.txt


Crear archivo .env

DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=finaldb

Crear la base de datos

SOURCE actors.sql;


Ejecutar el backend (FastAPI)
uvicorn main:app --reload


Ejecutar Streamlit
streamlit run app.py


**Funcionalidades principales**

✔ Cargar Excel y enviar datos a la API

Desde Streamlit puedes seleccionar un archivo .xlsx con diversas hojas y cargarlo directamente en la BD mediante solicitudes POST hacia FastAPI.


✔ CRUD completo para:

Actores

Teatros

Funciones

Roles

Entradas

Asistencias


✔ Consultas avanzadas

Ejemplos:

Entradas más caras

Entradas más baratas

Recaudación por teatro

Actores sin función

Funciones con entradas

Total de asistencia

Total de entradas por función


✔ Visualización en Streamlit

Tablas

DataFrames

Información procesada en tiempo real



