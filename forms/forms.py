from logging import PlaceHolder
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,EmailField,SubmitField,FileField,TextAreaField
from wtforms.validators import DataRequired

class FormEjemplo(FlaskForm):
# El argumento validators es opcional. Se utiliza para incluir validaciones en los campos.
# DataRequired verifica que el campo no esté vacío al momento de enviarlo.
    #          TIPO DE DATO , LABEL, VALIDADORES INDICA QUE ES REQUIRIDO Y EL MENSAJE A MOSTRAR
    usuario = EmailField('Usuario', validators=[DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Campo vacio ')])
    recordar=BooleanField('Recordar')
    submit=SubmitField('Enviar')
        
class FormLogin(FlaskForm):
    usuario = EmailField('Usuario', validators=[DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Campo vacio ')])
    submit=SubmitField('Login')
    
class FormRegister(FlaskForm):
    name = StringField('Usuario', validators=[DataRequired(message='Este campo es requerido')])
    email = EmailField('Correo', validators=[DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Campo vacio ')])
    submit=SubmitField('Registrarce')
    

class FormMensaje(FlaskForm):
    # tipo text area
    
    asunto = StringField('Asunto', validators=[DataRequired(message='Este campo es requerido')])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(message='Este campo es requerido')])
    submit=SubmitField('Envíar')

class FormPassword(FlaskForm):
    actual= PasswordField('Contraseña Actual', validators=[DataRequired(message='Este campo es requerido')])
    nueva= PasswordField('Nueva contraseña')
    confNueva= PasswordField('Confirme la contraseña')
    submit=SubmitField('Cambiar contraseña')
    
class FormProfile(FlaskForm):
    about = StringField('Acerca de mi')
    company = StringField('compañia')
    job = StringField('Puesto')
    celular = StringField('celular')
    country = StringField('Pais')
    img =FileField(u'img')
    btnEnviar=SubmitField('Guardar cambios')
    
