import controller
from flask import Flask,render_template,request # render_template redirecciona a un archivo html especificado
import hashlib # hashlib sirve para encriptar las contraseñas
from datetime import datetime # para el tiempo
import EnvioEmail # importar el archivo EnvioEmail.py


app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template('login.html')

# methods indica los posibles metodos  de envio de datos
@app.route("/validarUsuario",methods=["GET", "POST"])
# El nombre de la función es el mismo nombre del metodo del fomulario, es decir que al envíar el formulario se ejecutará esta función
def validarUsuario():
    # recibir  los datos
    if request.method == "POST": # para saber el tipo de metodo de respueta 
        
        usuario = request.form["usuario"] # request.form["nombre del campo"] - recibe los datos del campo del fomulario especificado, es decir el name
        contrasena = request.form["password"]# constraseña sin encriptar
        
        # encriptar la contraseña
        password_codificada=contrasena.encode() # organiza la contrasña
        # hay diferentes metodos en hashlib para encriptar la contraseña
        password_codificada = hashlib.sha256(password_codificada).hexdigest() # encripta la contraseña
        
        # respuesta true or false  si es correcto lo ingresado
        validacion = controller.validarUsuarioDB(usuario,password_codificada)
        
        # si es correcto la contraseña y el usuario
        if validacion == True:
            Destinatarios=controller.ListaDestinatarios(usuario) # trae la lista de todos los destinatarios menos el logueado 
            numero_destinatarios=len(Destinatarios) 
            Destinatarios.append(numero_destinatarios) # se agrega el numero de destinatarios al final de la lista
            
            return render_template('index.html',destinatarios=Destinatarios) 
        else :
            mensajeError= "Error de autenticación - Usuario o contraseña incorrectos -verifique los datos ingresados"
            # envíar el mensaje a la  plantilla html
            return render_template('informacion.html',mensajes=mensajeError)
            
                
# methods indica los posibles metodos  de envio de datos
@app.route("/RegistrarUsuario",methods=["GET", "POST"])
# El nombre de la función es el mismo nombre del metodo del fomulario, es decir que al envíar el formulario se ejecutará esta función
def RegistrarUsuario():
    # recibir  los datos
    if request.method == "POST": # para saber el tipo de metodo de respueta 
        
        nombre = request.form["txtnombre"] # request.form["nombre del campo"] - recibe los datos del campo del fomulario especificado, es decir el name
        email= request.form["txtusuarioregistro"]
        contrasena = request.form["txtpassregistro"]# constraseña sin encriptar
        
        # encriptar la contraseña
        password_codificada=contrasena.encode() # organiza la contrasña
        # hay diferentes metodos en hashlib para encriptar la contraseña
        password_codificada = hashlib.sha256(password_codificada).hexdigest() # encripta la contraseña
        
        # generar código de activación
        # el codigo es la fecha y hora actual (cuando se registra el usuario)
        codigoActivacion=datetime.now().strftime("%Y%m%d%H%M%S") # strftime formate la fecha y hora, así no tiene - : . ni espacios
                
        # pasarle al controller los datos para registrar el usuario
        controller.registrarUsuarioDB(nombre,password_codificada,email,codigoActivacion)
        
        # enviar el correo con el codigo de activación
        asuntoEmail="Activación de cuenta"
        mensajeEmail="MENSAJERÍA ELECTRÓNICA \n\n Sr "+nombre+",  su código de activacion es :\n\n"+codigoActivacion+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        
        # TODO al desplegar el proyecto descomentar enviarEmail
        # EnvioEmail.enviar(email,mensajeEmail,asuntoEmail) 
        
        mensaje= f"Usuario {nombre} registrado correctamente"
        return render_template('informacion.html',mensajes=mensaje)
               
# methods indica los posibles metodos  de envio de datos
@app.route("/ActivarUsuario",methods=["GET", "POST"])
# El nombre de la función es el mismo nombre del metodo del fomulario, es decir que al envíar el formulario se ejecutará esta función
def ActivarUsuariorUsuario():
    # recibir  los datos
    if request.method == "POST": # para saber el tipo de metodo de respueta 
        
        codigoIngresado = request.form["txtcodigo"] # request.form["nombre del campo"] - recibe los datos del campo del fomulario especificado, es decir el name
       

        # pasarle al controller los datos para registrar el usuario
        resultado=controller.ActivarUsuarioDB(codigoIngresado)
        
        # si trae resultado de  la consulta es porque el codigo es correcto y se activa el usuario
        if(len(resultado)>0):       
            mensaje= "Usuario activado"
            return render_template('informacion.html',mensajes=mensaje)
            
        else:
            mensaje="Código incorrecto"
            return render_template('informacion.html',mensajes=mensaje)
            
            
        
        
       