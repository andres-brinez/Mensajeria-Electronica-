# postgres
import psycopg2
# se debe instalae psycopg2 para trabajar con la base de datos postgres, para usar otra base de datos se  utiliza otra libreria

def conexionDB():
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="MensajeriaElectronica",
        user="postgres",
        password="admin"
        )
        print("Conexion exitosa")
        
        return conn
        
    
    except Exception as error:
        print("Error Conexión",error )
                                    # conexion con la base de datos
    
    

def validarUsuarioDB(usuario,contrasena):
  
    try:
        
        conexion=conexionDB()
        
        conexion.autocommit = True 
        
        # crear cursor el cual es el que ejecuta las consultas sql
        cursor = conexion.cursor()
        
        # sentencia sql para validar el usuario
        sql= "SELECT * FROM usuarios WHERE correo= '"+usuario+"' AND password= '"+contrasena+"';"
        print(sql)
        # ejecutar sentencia 
        cursor.execute(sql)
        
        # se obtiene lo datos
        resultado=cursor.fetchall()
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            return True # existe 
        else :
            return False # no existe
        
        
        
        # # mostrar los datos
        # print("Datos ")
        # for usuario in resultado:
        #     print(usuario)
            
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))


def registrarUsuarioDB(usuario,contrasena,email):
    try:
        
        conexion=conexionDB()
        
        conexion.autocommit = True 
        
        # crear cursor el cual es el que ejecuta las consultas sql
        cursor = conexion.cursor()
        
        # sentencia sql para registrar usuario
        sql= "INSERT INTO usuarios (usuario,password,correo) VALUES ('"+usuario+"','"+contrasena+"','"+email+"');"
        
        # ejecutar sentencia 
        cursor.execute(sql)
        
    except Exception as e:
        print("Error al traer los datos: " + str(e))    
    



