import sqlite3 as sql
from flask import session
from datetime import datetime 
# from utils import EnvioEmail
import hashlib # hashlib sirve para encriptar las contraseñas

def conexionDB():
    """ SE CONECTA CON LA BASE DE DATOS """
    try:
        
        con =sql.connect('DB.db')

        print('Conexion exitosa')
        return con
            
    except Exception as error:
        print("Error Conexión",error )
        
def ejecutarSentenciaSQL(sql):
    try:
        conexion=conexionDB()
        
        cursor=conexion.cursor()#  cursor el cual es el que ejecuta las consultas sql
        
        cursor.execute(sql) # ejecuta la sentencia
        print('Sentencia ejecutada')
        
        conexion.commit() # realiza la sentencia sql
       
        resultado=cursor.fetchall()
        
        return resultado
                    
    except Exception as e:
        print("Error al ejecutar la sentencia: " + str(e))  
        return False 
    
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
        sql= "INSERT INTO usuarios (name,password,correo) VALUES ('"+usuario+"','"+ password_codificada+"','"+email+"');"
        print(sql)
        ejecutarSentenciaSQL(sql)
        sql="INSERT INTO perfil (usuarioEmail)Values ('"+email+"');"# para el perfil
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        if len(resultado)==0:
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
        print(sql)
        # ejecutar sentencia y obtenes resultado
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            # borra las  sesiones anteriores
            session.clear();
        
            # crear la sesión del usuario logeado
            # se  puede guardar lo que quiera del usuario logeado
            session['id']=resultado[0][0]
            session['userName']=resultado[0][1]
            session['email']=resultado[0][3]
            print(session)
            return True # existe 
        
        else :
            return False # no existe
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        
def MensajesEnviados(origen):
      
    try:
        
        sql= "SELECT \"mensajeID\", u.\"name\",asunto,fecha FROM mensajes m  JOIN usuarios u ON m.\"to\"  = u.id WHERE \"from\" = '"+origen+"' ORDER BY fecha DESC ;"
        #selecciona los destinatarios (usuarios) que no sean el usuario logueado

        print(sql)
        
        resultado=ejecutarSentenciaSQL(sql)
        print(resultado)
                
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            return resultado # existen mensajes
        else :
            return 'no mensajes' # no hay mensajes 
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        
def MensajesRecibidos(origen):
    try:
        """ UTILICÉ EL JOIN ON PARA UNIR LA TABLA DE USAURIOS Y MENSAJES Y ASI PODER CAMBIAR EL ID DEL USUARIO QUE RECIBE POR SU NOMBRRE PARA PODERLO MOSTRAR EN EL FRONT """
        
        sql= "SELECT \"mensajeID\",\"from\",asunto,fecha,u.\"name\" FROM mensajes m  JOIN usuarios u ON m.\"to\"  = u.id WHERE \"name\" = '"+origen+"' ORDER BY fecha DESC ;"
        print(sql)
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            return resultado # existe 
        else :
            return 'no mensajes' # no existe
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        
def DeleteMensaje(id):
    try:
        sql= "DELETE FROM mensajes WHERE \"mensajeID\" = "+id+";"
        print(sql)
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        return True
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        return False
                
def ListaDestinatarios(idUsuario):
      
    try:
        
        print(idUsuario)
        #selecciona los destinatarios (usuarios) que no sean el usuario logueado
        sql= f"SELECT id,name FROM usuarios WHERE id != {idUsuario};"
        
        resultado= ejecutarSentenciaSQL(sql)
        print(f'destinatarios {resultado}')
        
        return resultado
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        
def guardarMensaje(destinoID,mensaje,asunto ):
    try:
        
        fecha=datetime.now().strftime("%d-%m-%Y")
        origenID=str(session['userName'])
        
        print(fecha)
        print(f' mensaje origen: {origenID}')
        
        sql="insert into mensajes (\"from\",\"to\",asunto,mensaje,fecha) values ('"+origenID+"','"+destinoID+"','"+asunto+"','"+mensaje+"','"+fecha+"');"
        print(sql)
        
        print('guardando mensaje')
        
        resultado=ejecutarSentenciaSQL(sql)
        
        print('resultado',resultado)
        
        if resultado==False:
            return  False
        
        return True
        
    except Exception as e:
        print("Error Guardar mensaje: " + str(e)) 
        return False 

def verMensaje(idMensaje):  
    try:
        
    
        # sentencia sql para validar el usuario
        sql= "SELECT * FROM mensajes WHERE mensajeID= "+idMensaje+";"
        print(sql)
        # ejecutar sentencia y obtenes resultado
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            
            return resultado # existe 
        
        else :
            return False # no existe
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        return False
             
def UpdateMensaje(idMensaje,asunto,mensaje,destinatario):
    try:

        sql= "UPDATE mensajes   SET asunto='"+asunto+"',mensaje='"+mensaje+"',\"to\"="+destinatario+"  WHERE \"mensajeID\" = "+idMensaje+";"
        print(sql)
        resultado= ejecutarSentenciaSQL(sql)
        print(resultado)
        
        if resultado==False:
            return False
        else:
            return True
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        return False
               
def verPerfil(correo):
    try:
        
        sql= "SELECT * from perfil p JOIN usuarios u ON u.correo  = p.email WHERE u.id  = '"+correo+"';"
        #selecciona los destinatarios (usuarios) que no sean el usuario logueado

        print(sql)
        
        resultado=ejecutarSentenciaSQL(sql)
        print(resultado)
                
        
        # para indicar si existe  o no existe
        # si en la consula a la base de datos trae  una respuesta con datos es que existe  y si no trae datos  no existe
        if (len(resultado)>0):
            print(resultado)

            return resultado
        else :
            return 'no existe ese perfil' 
    
    except Exception as e:
        print("Error al traer los datos: " + str(e))
        