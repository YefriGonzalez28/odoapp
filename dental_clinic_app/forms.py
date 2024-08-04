from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repita la Contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Roles', choices=[('admin', 'Administrador'), ('recp', 'Recepción'), ('doc', 'Odontólogo')], validators=[DataRequired()])
    submit = SubmitField('Registrar')

class AppointmentForm(FlaskForm):
    patient_name = StringField('Nombre del Paciente', validators=[DataRequired()])
    date = DateTimeField('Fecha y Hora de la Cita', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    doctor = StringField('Doctor', validators=[DataRequired()])
    code = StringField('Código', validators=[DataRequired()])
    affiliation = StringField('Afiliación', validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    subject = StringField('Asunto', validators=[DataRequired()])
    submit = SubmitField('Programar Cita')