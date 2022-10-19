from logging import PlaceHolder
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,EmailField
from wtforms.validators import DataRequired

class FormEjemplo(FlaskForm):
# El argumento validators es opcional. Se utiliza para incluir validaciones en los campos.
# DataRequired verifica que el campo no esté vacío al momento de enviarlo.
    #          TIPO DE DATO , LABEL, VALIDADORES INDICA QUE ES REQUIRIDO Y EL MENSAJE A MOSTRAR
    usuario = EmailField('Usuario', validators=[DataRequired(message='Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Campo vacio ')])
