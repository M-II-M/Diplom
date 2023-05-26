<<<<<<< Updated upstream
import os
import uuid

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from freel import forms
from freel.DocView import DocView

db = SQLAlchemy()
# конфиг
DATABASE = '/tmp/fhsite.db',
DEBAG = True,
SECRET_KEY = "powerful secretkey",
WTF_CSRF_SECRET_KEY = "a csrf secret key"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

# лоигн
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

# редактор
ckeditor = CKEditor(app)
app.config['UPLOAD_FOLDER'] = 'upload'

ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    """ Функция проверки расширения файла(пока только docx) """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def main_page():
    """ Главная """
    return render_template("main_page.html", )


@app.route("/ready_template", methods=["POST", "GET"])
def ready_template():
    """ Страница при выборе готового шаблона """
    return render_template("ready_template.html", )


@app.route("/prepare_template", methods=["POST", "GET"])
def prepare_template():
    """ Страница для подготовки шаблона """
    return render_template("prepare_template.html", )


@app.route("/editor", methods=["POST", "GET"])
def doc_editor():
    """ Редактор документа """
    form = forms.SelectAudioForm()
    if form.validate_on_submit():
        print(form.select_type.data)
    else:
        print(form.errors)
    return render_template('editor.html', form=form)


@app.route('/doc', methods=["POST", "GET"])
def index():
    """ Преобразование документа """
    form = forms.WordViewForm()

    test = DocView('test.docx')
    test.get_checkpoints()

    form.body.data = test.interim_code
    return render_template("editor.html", form=form)


@app.route('/save-record', methods=['POST'])
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
def test2():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
>>>>>>> Stashed changes
