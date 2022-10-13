# Importar el objeto Flask desde el paquete flask.

from flask import Flask,render_template

""" Crear instancia de aplicación Flask con el nombre app. Pasa la variable especial __name__ que
contiene el nombre del módulo Python actual. Se utiliza para indicar a la instancia dónde está
ubicada. Necesitará hacerlo porque Flask configura algunas rutas en segundo plano. """
app = Flask(__name__)


""" RUTAS """
# El decorador route de la aplicación (app) es el encargado de decirle a Flask qué URL debe ejecutar con su correspondiente función.

@app.route('/') # Decorador que indica la ruta de la página. 
def hola_mundo(): # lo que realiza al acceder a  la ruta
    return render_template('index.html') # renderiza el template index.html
