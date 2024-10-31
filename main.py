from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Modelos de datos
class Actor(BaseModel):
    nombre: str
    fecha_nacimiento: str
    nacionalidad: str

class Teatro(BaseModel):
    nombre: str
    direccion: str
    ciudad: str

class Funcion(BaseModel):
    titulo: str
    fecha: str
    teatro_id: int
    precio: float

class Rol(BaseModel):
    nombre: str

class Entrada(BaseModel):
    funcion_id: int
    fecha_compra: str
    cantidad: int
    total: float

class Asistencia(BaseModel):
    funcion_id: int
    actor_id: int
    role_id: int

# Rutas para insertar datos
@app.post("/actores/")
def create_actor(actor: Actor):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO actores (nombre, fecha_nacimiento, nacionalidad) VALUES (%s, %s, %s)",
                (actor.nombre, actor.fecha_nacimiento, actor.nacionalidad))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Actor creado con éxito"}

@app.post("/teatros/")
def create_teatro(teatro: Teatro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teatros (nombre, direccion, ciudad) VALUES (%s, %s, %s)",
                (teatro.nombre, teatro.direccion, teatro.ciudad))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Teatro creado con éxito"}

@app.post("/funciones/")
def create_funcion(funcion: Funcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funciones (titulo, fecha, teatro_id, precio) VALUES (%s, %s, %s, %s)",
                (funcion.titulo, funcion.fecha, funcion.teatro_id, funcion.precio))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Función creada con éxito"}

@app.post("/roles/")
def create_rol(rol: Rol):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO roles (nombre) VALUES (%s)", (rol.nombre,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Rol creado con éxito"}

@app.post("/entradas/")
def create_entrada(entrada: Entrada):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entradas (funcion_id, fecha_compra, cantidad, total) VALUES (%s, %s, %s, %s)",
                (entrada.funcion_id, entrada.fecha_compra, entrada.cantidad, entrada.total))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Entrada creada con éxito"}

@app.post("/asistencias/")
def create_asistencia(asistencia: Asistencia):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asistencias (funcion_id, actor_id, role_id) VALUES (%s, %s, %s)",
                (asistencia.funcion_id, asistencia.actor_id, asistencia.role_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Asistencia creada con éxito"}

# Rutas para consultar datos
@app.get("/actores/")
def read_actors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actores")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.get("/funciones/")
def read_funciones():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funciones")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Más consultas
@app.get("/consultas/")
def consultar_datos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ejemplo de consulta con JOIN
    cursor.execute("""
        SELECT f.titulo, a.nombre, r.nombre
        FROM funciones f
        INNER JOIN asistencias a ON f.id = a.funcion_id
        LEFT JOIN roles r ON a.role_id = r.id
    """)
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows

# Otras consultas adicionales (max, min, avg)
@app.get("/entradas/max/")
def max_entrada():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(total) FROM entradas")
    max_total = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"max_total": max_total[0]}

@app.get("/entradas/min/")
def min_entrada():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(total) FROM entradas")
    min_total = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"min_total": min_total[0]}

@app.get("/entradas/avg/")
def avg_entrada():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(total) FROM entradas")
    avg_total = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"avg_total": avg_total[0]}
