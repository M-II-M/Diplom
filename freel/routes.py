import os
import uuid

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from freel.DocView import DocView
from freel import app, db, forms
from freel.models import User


@app.route("/", methods=["POST", "GET"])
def main_page():
    """ Главная """
    return render_template("main_page.html", )


@app.route("/ready_template", methods=["POST", "GET"])
@login_required
def ready_template():
    """ Страница при выборе готового шаблона """
    return render_template("ready_template.html", )


@app.route("/prepare_template", methods=["POST", "GET"])
@login_required
def prepare_template():
    """ Страница для подготовки шаблона """
    return render_template("prepare_template.html", )


@app.route("/editor", methods=["POST", "GET"])
@login_required
def doc_editor():
    """ Редактор документа """
    form = forms.SelectAudioForm()
    if form.validate_on_submit():
        print(form.select_type.data)
    else:
        print(form.errors)
    return render_template('editor.html', form=form)


@app.route('/doc', methods=["POST", "GET"])
@login_required
def doc():
    """ Преобразование документа """
    form = forms.WordViewForm()

    test = DocView('test.docx')
    test.get_checkpoints()

    form.body.data = test.interim_code
    return render_template("editor.html", form=form)


@app.route('/save-record', methods=['POST'])
@login_required
def save_record():
    """ Запись аудио """
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    # защита от пустых файлов
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    return render_template("test.html")


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    """ Обработчик закгрузки файлов """
    if request.method == 'POST':
        file = request.files['file']
        # защита от пустых файлов
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)

        if file:
            try:
                file_name = str(uuid.uuid4()) + ".docx"
                full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                file.save(full_file_name)

                flash("Документ загружен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка загрузки документа", "error")

    return redirect(url_for('ready_template'))


@app.route('/test2', methods=["POST", "GET"])
@login_required
def test2():
    return render_template("test.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    form = forms.LoginForm()
    login = form.login.data
    password = form.password.data

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            # next_page = request.args.get('next')
            return redirect(url_for('main_page'))

        else:
            flash('Неверный логин или пароль')
    else:
        flash('Пожалуйста, заполните поля')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    login = form.login.data
    password = form.password.data
    password2 = form.confirm.data

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните поля')
        elif password != password2:
            flash('Парольи не совпадают!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return
