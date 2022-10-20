# Importar el objeto Flask desde el paquete flask.
from flask import Flask,render_template
import os # Importar el módulo os para poder acceder a las variables de entorno.

from forms.forms  import * #  importar la carpeta de  los formularios con los formularios

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
    return render_template('login.html',form=form) # renderizar el template login.htmt 

# register
@app.route('/register',methods=['GET','POST'])
def register():
    form=FormRegister() # instanciar el formulario
    return render_template('register.html',form=form)

# inicio
@app.route('/inicio',methods=['GET','POST'])
def inicio():
    return 'inicio'




