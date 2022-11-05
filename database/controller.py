# postgres
import psycopg2
# se debe instalar psycopg2 para trabajar con la base de datos postgres, para usar otra base de datos se  utiliza otra libreria

def conexionDB():
    """ SE CONECTA CON LA BASE DE DATOS """
    try:
        
        conn = psycopg2.connect(
        host="localhost",
        database="Mensajeria Electronica",
        user="postgres",
        password="admin"
        )
        
        print("Conexion exitosa")
        
        return conn
        
    
    except Exception as error:
        print("Error Conexión",error )


def registrarUsuarioDB(usuario,contrasena,email,codigoActivacion):
    try:
        
        conexion=conexionDB()
        
        conexion.autocommit = True 
        
        # crear cursor el cual es el que ejecuta las consultas sql
        cursor = conexion.cursor()
        
        # sentencia sql para registrar usuario
        
        # sentencia sql para registrar usuario
        sql= "INSERT INTO usuarios (usuario,password,correo,"+'"codigoActivacion"'+") VALUES ('"+usuario+"','"+contrasena+"','"+email+"','"+codigoActivacion+"');"
        print(sql)
        # ejecutar sentencia 
        cursor.execute(sql)
        
    except Exception as e:
        print("Error al traer los datos: " + str(e))  