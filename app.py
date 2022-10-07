import controller
from flask import Flask,render_template,request
import hashlib
# render_template redirecciona a un archivo html especificado
# hashlib sirve para encriptar las contraseñas

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
            return render_template('index.html')
        else :
            mensajeError= "Error de autenticación - Usuario o contraseña incorrectos -verifique los datos ingresados"
            # envíar el mensaje a la  plantilla html
            return render_template('informacion.html',mensajes=mensajeError)
            
        
        # print(f"Usuario: {usuario} - Contraseña: {contrasena}, Contraseña codificada: {password_codificada}")
        
       

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
        
        # pasarle al controller los datos para registrar el usuario
        controller.registrarUsuarioDB(nombre,password_codificada,email)
        
        mensaje= "Usuario registrado correctamente"
        return render_template('informacion.html',mensajes=mensaje)
            
        
        
        
       