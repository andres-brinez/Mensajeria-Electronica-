from flask import Flask,render_template,request
# render_template redirecciona a un archivo html especificado
app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template('login.html')

# methods indica los posibles metodos  de envio de datos
@app.route("/validarUsuario",methods=["GET", "POST"])
def validarUsuario():
    # recibir  los datos
    if request.method == "POST": # para saber el tipo de metodo de respueta 
        usuario = request.form["usuario"] # request.form["nombre del campo"] - recibe los datos del campo del fomulario especificado, es decir el name
        contrasena = request.form["password"]
        print(f"Usuario: {usuario} - Contraseña: {contrasena}")
        return render_template('index.html')