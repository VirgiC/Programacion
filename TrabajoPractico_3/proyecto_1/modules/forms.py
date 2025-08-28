from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length 

class RegisterForm(FlaskForm):
    '''Este tipo de formularios permite validar el ingreso de datos,
    el formato de email, tamaño de contraseña y confirmación de contraseña'''
    username = StringField(label="Nombre de usuario", validators=[DataRequired()]) 
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    nombre = StringField(label="Nombre", validators=[DataRequired()])
    apellido = StringField(label="Apellido", validators=[DataRequired()])
    claustro_choices = [("estudiante", "Estudiante"), ("docente", "Docente"), ("PAyS", "PAyS")]
    claustro = SelectField(label="Claustro", choices=claustro_choices, validators=[DataRequired()])
    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=5), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField(label='Registro')


class LoginForm(FlaskForm):
    '''Formulario para validar el formato de email y confirmación de contraseña'''
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField(label='Ingresar')

    