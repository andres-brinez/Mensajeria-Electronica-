# Importar el objeto Flask desde el paquete flask.
from flask import Flask,render_template,redirect,url_for,flash,request,session
from werkzeug.utils import secure_filename # para subir las imagenes
import os # Importar el módulo os para poder acceder a las variables de entorno.
from forms.forms  import * #  importar la carpeta de  los formularios con los formularios
import controller as  DB
from utils import ordenarLista

# configuración imagenes
UPLOAD_FOLDER= os.path.abspath("static\img\profile")
# extenciones permitidad
ALLOWED_EXTENSIONS=set(["png","jpg","jpeg"])


# el session es creado al validar el usuario en el controller

""" Crear instancia de aplicación Flask con el nombre app. Pasa la variable especial __name__ que
contiene el nombre del módulo Python actual. Se utiliza para indicar a la instancia dónde está
ubicada. Necesitará hacerlo porque Flask configura algunas rutas en segundo plano. """

app = Flask(__name__)

""" Otra forma de trabajar con las url """
# if __name__=='__main__':
#    app.add_url_rule('ruta'view_func=funcion)
#    app.add_url_rule('/register' ,view_func=register)

def allowed_file(filename):
    # solo permite subir imagenes de ese tipo  de extenciones  
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

""" Callbacks: Métodos antes y despúes de las peticiones """
@app.before_request
def before_request():
    print("Antes de la petición")
    
@app.after_request
def after_request(response):
    print("Después de la petición")
    return response

    

app.secret_key = os.urandom(24) # Generar una clave secreta de 24 caracteres para el formulario.
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

""" RUTAS """
# El decorador route de la aplicación (app) es el encargado de decirle a Flask qué URL debe ejecutar con su correspondiente función.


# register
@app.route('/register',methods=['GET','POST'])
def register():
        
    # si se envía el formulario por el metodo post 
    if  request.method=='POST':
                
        # trae los datos del formulario
        #asigna el valor  valor enviado desde formulario a la variable
        nombre=request.form["name"]   
        email=request.form["email"]
        password=request.form["password"]
        
        registro= DB.registrarUsuarioDB(nombre,password,email) #devuelve true o false si pudo registrar usuario 

        if registro:
            return redirect(url_for('register',register='ok')) 
        
        else :
            return redirect(url_for('register',register='false'))

    else:
        print('registrando  usuario')
        form=FormRegister() # instanciar el formulario
        return render_template('register.html',form=form)
    

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
                    
            return redirect(url_for('inicio')) # redireccionar a la ruta 
        
        
        """ flash hace posible grabar un mensaje al final de una solicitud y
            acceder a él en la siguiente solicitud. """
        flash("Usuario o contraseña incorrecta ")
        return redirect(url_for('login')) # redireccionar a la ruta 
    
    return render_template('login.html',form=form) 

@app.route('/logout')
def logout():
    # borra los datos de  la sesión
    session.clear()
    return redirect(url_for('login'))

# inicio
@app.route('/',methods=['GET','POST'])
def inicio():
    
    if 'id' in session:
        userName=session['userName']
        print(userName)
        print(session['id'])

        Enviados=DB.MensajesEnviados(userName)
        Recibidos=DB.MensajesRecibidos(userName)
        print(Enviados)
        print(Recibidos)
        
        return render_template('index.html',messagesEnd=Enviados,messagesRecibidos=Recibidos)
    else:
        return render_template('accesoDenegado.html')
    
@app.route('/sendMessage',methods=['GET','POST'])
def sendMessage():
    # para saber si está logeado
    if 'id' in session:
        
        form=FormMensaje()

        if(form.validate_on_submit()):
            print("formulario enviado correctamente")
            
            idDestinatario = request.form["destino"] 
            mensaje = request.form["mensaje"] 
            asunto=request.form["asunto"]
            
            respuesta= DB.guardarMensaje(idDestinatario,mensaje,asunto)
            
            if respuesta==False:
                return redirect(url_for('inicio',mensaje='false'))

        
            else :
                return redirect(url_for('inicio',mensaje='ok')) 
            
            
        else:    
            idUsuario= session['id']
            print(f'id usuario {idUsuario}')
            listado=DB.ListaDestinatarios(idUsuario)
            print(listado)
            
            return render_template('sendMensaje.html',usuarios=listado,form=form)
    
    
        
    else:
        return render_template('accesoDenegado.html')
    
@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete(id=None):
    
    if DB.DeleteMensaje(id):
        return redirect(url_for('inicio', delete='true'))
    else:
        return redirect(url_for('inicio', delete='false'))

@app.route('/edit/<string:id>',methods=['GET','POST'])
def edit(id=None):


    # si está logeado
    if 'id' in session:

        print(id)
        form=FormMensaje()    

        # si se está pidiendo el formulario
        if request.method=='GET':
            idUsuario= session['id']

            respuesta=DB.ListaDestinatarios(idUsuario) #  trae los destinatarios como está en la base de datos

            mensaje=DB.verMensaje(id)[0] # trae el mensaje con el id
            
            # print(mensaje)
            
            toID=mensaje[5]

            destinatarios=ordenarLista.ordenar(respuesta,toID) # los ordena para que aparezca de primero el del id envíaddo

            if len(mensaje)>0:
                return render_template('editMensaje.html',form=form,usuarios=destinatarios,mensaje=mensaje)
            else:
                return redirect(url_for('inicio', edit='false'))


        
            # si se envía el formulario por el metodo post 
        elif  request.method=='POST':
            print('formulario enviado')

            idDestinatario = request.form["destino"] 
            mensaje = request.form["mensaje"] 
            asunto=request.form["asunto"]

            print('destinatario',idDestinatario)
            print('mensaje',mensaje)
            print('asunto',asunto)

            resultado=DB.UpdateMensaje(id,asunto,mensaje,idDestinatario)

            if resultado==True:
                return redirect(url_for('inicio', edit='true'))
            else:
                return redirect(url_for('inicio', edit='false'))

    else:
        return render_template('accesoDenegado.html')

      
       
@app.route('/profile/<string:id>',methods=['GET','POST'])
def profile(id=None):
    
    # si está logeado
    if 'id' in session:
        
        formPassword=FormPassword()
        formProfile=FormProfile()
        
        forms={
            'formPassword':formPassword,
            'formProfile':formProfile
        }
        

        if(formPassword.validate_on_submit()):
            print("formulario contraseña enviado correctamente")
            
            
            passwordActual = request.form["actual"]            
            passwordNueva = request.form["nueva"]
            passwordConfirmar=request.form["confNueva"]
            
            resultado= DB.changePassword(passwordActual,passwordNueva,passwordConfirmar)
            flash(resultado) 
            
                    
        elif formProfile.validate_on_submit():
            
            print("formulario perfil enviado correctamente")
            
            # obtiene los datos
            
            email=request.form['email']
            about= request.form['about']
            company= request.form['company']
            job= request.form['job']
            celular= request.form['celular']
            country= request.form['country']
            img= request.files['img']
            
            filename= secure_filename(img.filename)# obtiene el nombre de la imagen
            
            # si no se envía una imagen se  pone una por defecto 
            if len(filename)<=0:
                print(filename)
                # imagen  por defecto
                filename="profile-defecto.png"
                
            else:
                
                permitir_img= allowed_file(filename) # verifica si el archivo es de  una extención permitida
                
                if permitir_img==True:
                    
                    # guarda la imagen en la carpeta static
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    
                    flash('ERROR - Solo se permiten imagenes con extención .png, .jpg, .jpeg')
                    return redirect(url_for('profile',id=id))

                    
                    
            # guarda los datos en la base de datos
            resultado= DB.editProfile(email,about,company,job,celular,country,filename)
            flash(resultado)
            return redirect(url_for('profile',id=id))
        
        
        resultado=DB.verPerfil(id)[0]
        print(resultado)
        return render_template('profile.html', form=forms,profile=resultado)
    
            
    else:
        return render_template('accesoDenegado.html')
    

    
