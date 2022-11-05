# Importar el objeto Flask desde el paquete flask.
from flask import Flask,render_template,redirect,url_for,flash,request
import os # Importar el módulo os para poder acceder a las variables de entorno.
from forms.forms  import * #  importar la carpeta de  los formularios con los formularios
from database import controller as  DB
from utils import EnvioEmail


""" Crear instancia de aplicación Flask con el nombre app. Pasa la variable especial __name__ que
contiene el nombre del módulo Python actual. Se utiliza para indicar a la instancia dónde está
ubicada. Necesitará hacerlo porque Flask configura algunas rutas en segundo plano. """

app = Flask(__name__)

app.secret_key = os.urandom(24) # Generar una clave secreta de 24 caracteres para el formulario.

""" RUTAS """
# El decorador route de la aplicación (app) es el encargado de decirle a Flask qué URL debe ejecutar con su correspondiente función.

@app.route('/') # Decorador que indica la ruta de la página. 
def hola_mundo(): # lo que realiza al acceder a  la ruta
    return render_template('index.html',nombre="felipe") # renderiza el template index.html

# Ejemplo de formulario
@app.route('/form',methods=['GET','POST'])
def ejemploForm ():
    form=FormEjemplo() # instanciar el formulario
    return render_template('formularioEjemplo.html',form=form) # renderizar el template login.htmt 

# login
@app.route('/login',methods=['GET','POST'])
def login ():
    form=FormLogin() # instanciar el formulario

    # validar si el formulario fue envíado correctamente
    if(form.validate_on_submit()):
        print("formulario enviado correctamente")
        
        usuario=form.usuario.data # obtener el valor del campo usuario
                
        """ flash hace posible grabar un mensaje al final de una solicitud y
        acceder a él en la siguiente solicitud. """
        flash("Bienvenido "+usuario) #  mensaje de bienvenida
        return redirect(url_for('inicio')) # redireccionar a la ruta 
    
    return render_template('login.html',form=form) # renderizar el template login.htmt 

# # register
@app.route('/register',methods=['GET','POST'])
def register():
        
    # si se envía el formulario por el metodo post 
    if  request.method=='POST':
        
        form=FormRegister() # instanciar el formulario

        print('envio formulario')
        
        # trae los datos del formulario
        #asigna el valor  valor enviado desde formulario a la variable
        nombre=request.form["nombre"]   
        email=request.form["email"]
        password=request.form["password"]
        
        registro= DB.registrarUsuarioDB(nombre,password,email) #devuelve true o false si pudo registrar usuario 
        
        if registro:
            return redirect(url_for('register',register='ok')) # redireccionar a la ruta 
        
        else :
            return redirect(url_for('register',register='false')) # redireccionar a la ruta 

    else:
        print('registrando  usuario')
        return render_template('register.html',form=form)


# recuperación contraseñas
@app.route('/recuperacion',methods=['GET','POST'])
def RecuperarContrasena():
    form=FormRegister() # instanciar el formulario
    # return render_template('register.html',form=form)
    return 'aquí va la recuperación de contraseñas'

# inicio
@app.route('/inicio',methods=['GET','POST'])
def inicio():
    return render_template('index.html')




