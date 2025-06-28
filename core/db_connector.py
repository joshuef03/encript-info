import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("DATABASE_PASSWORD"),
            database='encript_info'
        )
        return conexion
    except Error as e:
        raise RuntimeError(f"Error al conectar con MySQL: {e}")

def insertar_archivo(file_name: str, binary_data: bytes):
    conexion = conectar_db()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO archivos_encriptados (file_name, data)
                VALUES (%s, %s)
            """, (file_name, binary_data))
        conexion.commit()
    finally:
        conexion.close()

def obtener_archivos():
    conexion = conectar_db()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, file_name FROM archivos_encriptados")
            return cursor.fetchall()
    finally:
        conexion.close()

def descargar_archivo(id_archivo: int):
    conexion = conectar_db()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT file_name, data FROM archivos_encriptados WHERE id = %s", (id_archivo,))
            return cursor.fetchone()
    finally:
        conexion.close()