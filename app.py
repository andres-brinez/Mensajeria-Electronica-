# Importar el objeto Flask desde el paquete flask.
from flask import Flask,render_template,redirect,url_for,flash,request,session
import os # Importar el módulo os para poder acceder a las variables de entorno.
from forms.forms  import * #  importar la carpeta de  los formularios con los formularios
from database import controller as  DB
from utils import EnvioEmail

idRegistrado=''

# el session es creado al validar el usuario en el controller

""" Crear instancia de aplicación Flask con el nombre app. Pasa la variable especial __name__ que
contiene el nombre del módulo Python actual. Se utiliza para indicar a la instancia dónde está
ubicada. Necesitará hacerlo porque Flask configura algunas rutas en segundo plano. """

app = Flask(__name__)

app.secret_key = os.urandom(24) # Generar una clave secreta de 24 caracteres para el formulario.

""" RUTAS """
# El decorador route de la aplicación (app) es el encargado de decirle a Flask qué URL debe ejecutar con su correspondiente función.

# login
@app.route('/login',methods=['GET','POST'])
def login ():
    form=FormLogin() # instanciar el formulario

    # validar si el formulario fue envíado correctamente
    if(form.validate_on_submit()):
        print("formulario enviado correctamente")
        
        usuario=form.usuario.data 
        password=form.password.data  
        
        if DB.validarUsuarioDB(usuario,password): # si devuelve true
            
            global idRegistrado
            idRegistrado=session['id'] # para poder usar la variable global
        
            
            return redirect(url_for('inicio')) # redireccionar a la ruta 
        
        
        """ flash hace posible grabar un mensaje al final de una solicitud y
            acceder a él en la siguiente solicitud. """
        flash("Usuario o contraseña incorrecta ")
        return redirect(url_for('login')) # redireccionar a la ruta 

    
    return render_template('login.html',form=form) # renderizar el template login.htmt


# # register
@app.route('/register',methods=['GET','POST'])
def register():
        
    # si se envía el formulario por el metodo post 
    if  request.method=='POST':
        

        print('envio formulario')
        
        # trae los datos del formulario
        #asigna el valor  valor enviado desde formulario a la variable
        nombre=request.form["name"]   
        email=request.form["email"]
        password=request.form["password"]
        
        registro= DB.registrarUsuarioDB(nombre,password,email) #devuelve true o false si pudo registrar usuario 
        
        if registro:
            return redirect(url_for('register',register='ok')) # redireccionar a la ruta 
        
        else :
            return redirect(url_for('register',register='false')) # redireccionar a la ruta 

    else:
        print('registrando  usuario')
        form=FormRegister() # instanciar el formulario
        return render_template('register.html',form=form)


# inicio
@app.route('/inicio',methods=['GET','POST'])
def inicio():
    
    if 'id' in session:
        userName=session['userName']
        print(userName)
        print(session['id'])

        Enviados=DB.MensajesEnviados(userName)
        Recibidos=DB.MensajesRecibidos(userName)
        
        return render_template('index.html',messagesEnd=Enviados,messagesRecibidos=Recibidos)
    else:
        return render_template('accesoDenegado.html')


@app.route('/endMessage',methods=['GET','POST'])
def endMessage():
    
    print(f'id registrado {idRegistrado}')
    
    if 'id' in session:
    
        idUsuario= session['id']
        print(f'id usuario {idUsuario}')
        listado=DB.ListaDestinatarios(idUsuario)
        print(listado)
    else:
        return 'inicia sesión para poder acceder a está página    '
    
    # si se envía el formulario por el metodo post 
    if  request.method=='POST':
        print('formulario enviado')
        idDestinatario = request.form["destino"] 
        mensaje = request.form["mensaje"] 
        asunto=request.form["asunto"]
        
        print(idDestinatario)
        print(mensaje)
        print(asunto)
        
        DB.guardarMensaje(idDestinatario,mensaje,asunto)
        
        
        return 'mensaje envíado'    
            
    return render_template('endMensaje.html',usuarios=listado)

@app.route('/edit',methods=['GET','POST'])
def edit():
    
    print(f'id registrado {idRegistrado}')
    
    if 'id' in session:
    
        idUsuario= session['id']
        print(f'id usuario {idUsuario}')
        listado=DB.ListaDestinatarios(idUsuario)
        print(listado)
    else:
        return 'inicia sesión para poder acceder a está página    '
    
    # si se envía el formulario por el metodo post 
    if  request.method=='POST':
        print('formulario enviado')
        idDestinatario = request.form["destino"] 
        mensaje = request.form["mensaje"] 
        asunto=request.form["asunto"]
        
        print(idDestinatario)
        print(mensaje)
        print(asunto)
        
        DB.guardarMensaje(idDestinatario,mensaje,asunto)
        
        """ render_template('endMensaje.html',usuarios=listado) """
        return 'mensaje envíado'    
            
    return  'editar mensaje'

@app.route('/delete',methods=['GET','POST'])
def delete():
    return 'delete mensaje'

    
    
    
    







