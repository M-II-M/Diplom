from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired


class WordViewForm(FlaskForm):
    body = CKEditorField('Body')  # <--
    submit = SubmitField('Загрузить')


class SelectAudioForm(FlaskForm):
    select_type = RadioField('Label', choices=[('1', 'Записать сейчас'),
                                               ('2', 'Загрузить готовую запись')])


class SelectDocForm(FlaskForm):
    select_type = RadioField('Label', choices=[('1', 'Загрузить готовый шаблон'),
                                               ('2', 'Создать шаблон')])


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    login = StringField('Введите логин', [validators.Length(min=4, max=25)])
    password = PasswordField('Введите пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Повторите пароль')
    submit = SubmitField("Подтвердить")


