from datetime import datetime
import os
import uuid

from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from freel.DocView import DocView
from freel import app, db, forms
from freel.models import User, Files, UserTemplates


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


@app.route("/audio_choice", methods=["POST", "GET"])
@login_required
def audio_choice():
    """ Выбор типа загрузки аудио """
    return render_template("audio_choice.html", )


@app.route('/editor?<template_type>', methods=["POST", "GET"])
@login_required
def editor(template_type):
    """ Преобразование документа """
    form = forms.WordViewForm()

    desc = ''
    if template_type == 'ready_template':
        desc = "Вы можете изменить шаблон или сразу перейти к речевому заполнению"
    elif template_type == 'prepare_doc':
        desc = "Подготовте шаблон и переходите к речевому заполнению"

    # TODO написать гайд по выделению

    # Отображение шаблона в редакторе
    doc_view = DocView(session.get(template_type))
    doc_view.word2html()
    form.body.data = doc_view.html

    return render_template("editor.html", form=form, template_type=template_type, desc=desc)


@app.route('/audio_record', methods=["POST", "GET"])
@login_required
def audio_record():
    """ Запись аудио """
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        # if "audio_data" not in request.files:
        #     return redirect(request.url)

        file = request.files["audio_data"]
        if file.filename == "":
            return redirect(request.url)

        # Запись на сервер
        file_name = session['ready_template'][0:-6] + ".mp3"
        file.save(file_name)
        print(file_name)

        session['audio'] = file_name

    return render_template("audio_record.html")


@app.route('/upload_ready_template', methods=["POST", "GET"])
@login_required
def upload_ready_template():
    """ Обработчик закгрузки файлов """
    if request.method == 'POST':
        file = request.files['file']
        # Защита от пустых файлов
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)

        if file:
            try:
                # Сохранение файла в папку(имя папки соответсвует имени файла)
                file_name = str(uuid.uuid4()) + ".docx"
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + file_name[0:-6]))
                full_file_name = os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + file_name[0:-6], file_name)
                file.save(full_file_name)

                # Сохранение шаблона в бд
                save_template = Files(path=full_file_name,
                                      file_name=file.filename,
                                      file_type="template",
                                      data=datetime.now())
                db.session.add(save_template)
                db.session.commit()

                template_id = db.session.query(Files).filter(Files.path == full_file_name).one()
                user_template = UserTemplates(user_id=current_user.get_id(),
                                              template_id=template_id.id)
                db.session.add(user_template)
                db.session.commit()

                session['ready_template'] = full_file_name

                flash("Документ загружен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка загрузки документа", "error")

    return redirect(url_for('editor', template_type='ready_template'))


@app.route('/upload_prepare_doc', methods=["POST", "GET"])
@login_required
def upload_prepare_doc():
    """ Обработчик закгрузки файлов """
    if request.method == 'POST':
        file = request.files['file']
        # Защита от пустых файлов
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)

        if file:
            try:
                # Сохранение файла в папку(имя папки соответсвует имени файла)
                file_name = str(uuid.uuid4()) + ".docx"
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + file_name[0:-6]))
                full_file_name = os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + file_name[0:-6], file_name)
                file.save(full_file_name)

                # Сохранение шаблона в бд
                save_template = Files(path=full_file_name,
                                      file_name=file.filename,
                                      file_type="prepare",
                                      data=datetime.now())
                db.session.add(save_template)
                db.session.commit()

                session['prepare_doc'] = full_file_name

                flash("Документ загружен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка загрузки документа", "error")

    return redirect(url_for('editor', template_type='prepare_doc'))


@app.route('/template_processing?<template_type>', methods=["POST", "GET"])
@login_required
def template_processing(template_type):
    """ Обработка шаблона из редактора"""
    # Перезаписываем файл с использованием данных из редактора
    if request.method == 'POST':
        template_with_chekpoints = DocView(session.get(template_type))
        template_with_chekpoints.word2html()
        template_with_chekpoints.get_checkpoints()
        template_with_chekpoints.save_interim_template_html()
        template_with_chekpoints.save_interim_template_docx()

        # если документ подготовили, записать его в шаблоны
        if template_type == 'prepare_doc':
            template_id = db.session.query(Files).filter(Files.path == session['prepare_doc']).one()
            user_template = UserTemplates(user_id=current_user.get_id(),
                                          template_id=template_id.id)
            db.session.add(user_template)
            db.session.commit()

    else:
        print('barabuh')

    return redirect(url_for('audio_choice'))


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

# @app.after_request
# def redirect_to_signin(response):
#     if response.status_code == 401:
#         return redirect(url_for('login_page') + '?next=' + request.url)
#
#     return
