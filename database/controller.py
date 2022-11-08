# postgres
import psycopg2
# se debe instalar psycopg2 para trabajar con la base de datos postgres, para usar otra base de datos se  utiliza otra libreria

from flask import session
from datetime import datetime # para el tiempo
from utils import EnvioEmail
import hashlib # hashlib sirve para encriptar las contraseñas


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
        
def ejecutarSentenciaSQL(sql):
    
    conexion=conexionDB() # conexión con la base de datos
        
    conexion.autocommit = True  # para guardar la sentencia 

    # crear cursor el cual es el que ejecuta las consultas sql
    cursor = conexion.cursor()
        
    # ejecutar sentencia 
    cursor.execute(sql)
    
    try:
        # se obtiene lo datos si devuelve algo la sentencia
        resultado=cursor.fetchall()
            
        return resultado
        
    except Exception as e:
        print('no hay resultado de la sentencia')
    
def registrarUsuarioDB(usuario,contrasena,email,):
    try:
        
        # generar código de activación
        # el codigo es la fecha y hora actual (cuando se registra el usuario)
        codigoActivacion=datetime.now().strftime("%Y%m%d%H%M%S") # strftime formate la fecha y hora, así no tiene - : . ni espacios
            
        # enviar el correo con el codigo de activación
        asuntoEmail="Activación de cuenta"
        mensajeEmail="MENSAJERÍA ELECTRÓNICA \n\n Sr "+usuario+",  su código de activacion es :\n\n"+codigoActivacion+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        
        # TODO descomentar para enviar email con codigo de activación
        # EnvioEmail.enviar(email,mensajeEmail,asuntoEmail)
        
        # encriptar la contraseña
        password_codificada=contrasena.encode() # organiza la contrasña
        # hay diferentes metodos en hashlib para encriptar la contraseña
        password_codificada = hashlib.sha256(password_codificada).hexdigest() # encripta la contraseña
            
        # sentencia sql para registrar usuario
        sql= "INSERT INTO usuarios (estado,name,password,correo,"+'"codigoActivacion"'+") VALUES ('false','"+usuario+"','"+ password_codificada+"','"+email+"','"+codigoActivacion+"');"
        
        ejecutarSentenciaSQL(sql)
        
    
        return True
        
    except Exception as e:
        print("Error al Registrar usuario: " + str(e))  
        return False 
    
# validar si el usuario existe
def validarUsuarioDB(usuario,contrasena):    
    try:
        
        # encriptar la contraseña para compararla con la de la base de datos
        password_codificada=contrasena.encode() # organiza la contrasña
        # hay diferentes metodos en hashlib para encriptar la contraseña
        password_codificada = hashlib.sha256(password_codificada).hexdigest() # encripta la contraseña
        
        # sentencia sql para validar el usuario
        sql= "SELECT * FROM usuarios WHERE correo= '"+usuario+"' AND password= '"+password_codificada+"';"
        
        # ejecutar sentencia y obtenes resultado
        resultado= ejecutarSentenciaSQL(sql)
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            # borra las  sesiones anteriores
            session.clear();
        
            # crear la sesión del usuario logeado
            # se  puede guardar lo que quiera del usuario logeado
            session['id']=resultado[0][0]
            session['userName']=resultado[0][1]
            
            print(session)
            print(len(session))
            return True # existe 
        
        else :
            return False # no existe
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        

def ListaDestinatarios(idUsuario):
      
    try:
        
        #selecciona los destinatarios (usuarios) que no sean el usuario logueado
        sql= f"SELECT name FROM usuarios WHERE id != {idUsuario};"
        
        resultado= ejecutarSentenciaSQL(sql)
        
        print(resultado)
        
        return resultado
    
        # # mostrar los datos
        # print("Datos ")
        # for usuario in resultado:
        #     print(usuario)
            
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        
        
def guardarMensaje(destinoID,mensaje,asunto ):
    try:
    
        
        # sql="insert into mensajeria ("+'asunto'+",mensaje,correo_origen,correo_destino,fecha,hora,estado) values ('"+asunto+"','"+mensaje+"','"+emailOrigen+"','"+emailDestino+"','"+fecha+"','"+hora+"','send');"


        fecha=datetime.now().strftime("%d-%m-%Y")
        origenID=str(session['userName'])
        # origenID=str(14)
        print(fecha)
        print(f' mensaje origen: {origenID}')
        
        sql="insert into mensajes (\"from\",\"to\",asunto,mensaje,fecha) values ('"+origenID+"','"+destinoID+"','"+asunto+"','"+mensaje+"','"+fecha+"');"
        print(sql)
        # sql="insert into mensajeria ("'asunto '",mensaje,correo_origen,correo_destino,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+emailOrigen+"','"+emailDestino+"','send')"
        # print(sql)
        # print(emailDestino)
        # print(emailOrigen)
        
        ejecutarSentenciaSQL(sql)
        
    except Exception as e:
        print("Error Guardar mensaje: " + str(e))  