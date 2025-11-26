from fastapi import FastAPI, HTTPException, Query
import mysql
from pydantic import BaseModel
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


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


def read_query(query: str, params: tuple = ()):
    try:
        connection = connect(
            host="localhost",
            database="finaldb",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(e)
        return []



def execute_query(query, params=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar la consulta: {str(e)}")


def read_query(query, params=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                rows = cursor.fetchall()
                return rows
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")


@app.post("/actores/")
def create_actor(actor: Actor):
    query = "INSERT INTO actores (nombre, fecha_nacimiento, nacionalidad) VALUES (%s, %s, %s)"
    execute_query(query, (actor.nombre, actor.fecha_nacimiento, actor.nacionalidad))
    return {"message": "Actor creado con éxito"}

@app.post("/teatros/")
def create_teatro(teatro: Teatro):
    query = "INSERT INTO teatros (nombre, direccion, ciudad) VALUES (%s, %s, %s)"
    execute_query(query, (teatro.nombre, teatro.direccion, teatro.ciudad))
    return {"message": "Teatro creado con éxito"}

@app.post("/funciones/")
def create_funcion(funcion: Funcion):
    query = "INSERT INTO funciones (titulo, fecha, teatro_id, precio) VALUES (%s, %s, %s, %s)"
    execute_query(query, (funcion.titulo, funcion.fecha, funcion.teatro_id, funcion.precio))
    return {"message": "Función creada con éxito"}

@app.post("/roles/")
def create_rol(rol: Rol):
    query = "INSERT INTO roles (nombre) VALUES (%s)"
    execute_query(query, (rol.nombre,))
    return {"message": "Rol creado con éxito"}

@app.post("/entradas/")
def create_entrada(entrada: Entrada):
    query = "INSERT INTO entradas (funcion_id, fecha_compra, cantidad, total) VALUES (%s, %s, %s, %s)"
    execute_query(query, (entrada.funcion_id, entrada.fecha_compra, entrada.cantidad, entrada.total))
    return {"message": "Entrada creada con éxito"}

@app.post("/asistencias/")
def create_asistencia(asistencia: Asistencia):
    query = "INSERT INTO asistencias (funcion_id, actor_id, role_id) VALUES (%s, %s, %s)"
    execute_query(query, (asistencia.funcion_id, asistencia.actor_id, asistencia.role_id))
    return {"message": "Asistencia creada con éxito"}

# Rutas para consultar datos
@app.get("/actores/")
def read_actors():
    query = "SELECT * FROM actores"
    rows = read_query(query)
    return [{"id": row[0], "nombre": row[1], "fecha_nacimiento": row[2], "nacionalidad": row[3]} for row in rows]

@app.get("/teatros/")
def read_teatros():
    query = "SELECT * FROM teatros"
    rows = read_query(query)
    return [{"id": row[0], "nombre": row[1], "direccion": row[2], "ciudad": row[3]} for row in rows]

@app.get("/funciones/")
def read_funciones():
    query = "SELECT * FROM funciones"
    rows = read_query(query)
    return [{"id": row[0], "titulo": row[1], "fecha": row[2], "teatro_id": row[3], "precio": row[4]} for row in rows]

@app.get("/roles/")
def read_roles():
    query = "SELECT * FROM roles"
    rows = read_query(query)
    return [{"id": row[0], "nombre": row[1]} for row in rows]

@app.get("/entradas/")
def read_entradas():
    query = "SELECT * FROM entradas"
    rows = read_query(query)
    return [{"id": row[0], "funcion_id": row[1], "fecha_compra": row[2], "cantidad": row[3], "total": row[4]} for row in rows]

@app.get("/asistencias/")
def read_asistencias():
    query = "SELECT * FROM asistencias"
    rows = read_query(query)
    return [{"id": row[0], "funcion_id": row[1], "actor_id": row[2], "role_id": row[3]} for row in rows]

@app.get("/asistencias/")
def read_asistencias():
    query = "SELECT * FROM asistencias"
    rows = read_query(query)
    return [{"id": row[0], "funcion_id": row[1], "actor_id": row[2], "role_id": row[3]} for row in rows]

@app.get("/consultas/recaudacion_teatro")
def recaudacion_teatro():
    query = """
    SELECT teatros.id, teatros.nombre, MAX(entradas.total) AS max_recaudacion, MIN(entradas.total) AS min_recaudacion
    FROM teatros
    LEFT JOIN funciones ON teatros.id = funciones.teatro_id
    LEFT JOIN entradas ON funciones.id = entradas.funcion_id
    GROUP BY teatros.id, teatros.nombre;
    """
    rows = read_query(query)
    return [{"teatro_id": row[0], "nombre": row[1], "max_recaudacion": row[2], "min_recaudacion": row[3]} for row in rows]

@app.get("/consultas/total_asistencia")
def get_total_asistencia():
    query = """
    SELECT teatros.nombre AS teatro, COUNT(asistencias.id) AS total_asistencias
    FROM asistencias
    INNER JOIN funciones ON asistencias.funcion_id = funciones.id
    INNER JOIN teatros ON funciones.teatro_id = teatros.id
    GROUP BY teatros.nombre;
    """
    rows = read_query(query)
    return [{"teatro": row[0], "total_asistencia": row[1]} for row in rows]

@app.get("/consultas/entrada_mas_cara")
def get_entrada_mas_cara():
    query = """
    SELECT teatros.nombre AS teatro, funciones.titulo AS funcion, funciones.precio AS precio_entrada
    FROM funciones
    INNER JOIN teatros ON funciones.teatro_id = teatros.id
    WHERE funciones.precio = (
    SELECT MAX(precio) FROM funciones
    );
    """
    rows = read_query(query)
    return [{"teatro": row[0], "funcion": row[1], "precio_entrada":row[2]} for row in rows]

@app.get("/consultas/entrada_mas_barata")
def get_entrada_mas_barata():
    query = """
    SELECT teatros.nombre AS teatro, funciones.titulo AS funcion, funciones.precio AS precio_entrada
    FROM funciones
    INNER JOIN teatros ON funciones.teatro_id = teatros.id
    WHERE funciones.precio = (
    SELECT MIN(precio) FROM funciones
    );
    """
    rows = read_query(query)
    return [{"teatro": row[0], "funcion": row[1], "precio_entrada":row[2]} for row in rows]

@app.get("/consultas/total_entradas_funcion")
def total_entradas_funcion():
    query = """
        SELECT funciones.titulo, SUM(entradas.cantidad) AS total_entradas
        FROM funciones
        LEFT JOIN entradas ON funciones.id = entradas.funcion_id
        GROUP BY funciones.titulo
    """
    rows = read_query(query)
    return [{"titulo": row[0], "total_asistencia": row[1]} for row in rows]

@app.get("/consultas/sin_funcion")
def sin_funcion():
    query = """
        SELECT actores.nombre
        FROM actores
        LEFT JOIN asistencias ON actores.id = asistencias.actor_id
        WHERE asistencias.id IS NULL
    """
    rows = read_query(query)
    return [{"nombre": row[0], } for row in rows]

@app.get("/consultas/teatros_con_funciones")
def teatros_con_funciones():
    query ="""
        SELECT teatros.nombre AS teatro_nombre, COUNT(funciones.id) AS num_funciones
        FROM teatros
        LEFT JOIN funciones ON teatros.id = funciones.teatro_id
        GROUP BY teatros.nombre
    """
    rows = read_query(query)
    return [{"teatro_nombre": row[0],"num_funciones":row[1] } for row in rows]

@app.get("/consultas/funciones_con_entradas")
def funciones_con_entradas():
    query ="""
        SELECT funciones.titulo, SUM(entradas.cantidad) AS total_entradas
        FROM funciones
        LEFT JOIN entradas ON funciones.id = entradas.funcion_id
        GROUP BY funciones.titulo
    """
    rows = read_query(query)
    return [{"titulo": row[0],"total_entradas":row[1] } for row in rows]
