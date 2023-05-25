from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

ckeditor = CKEditor(app)
app.config['UPLOAD_FOLDER'] = 'upload'

ALLOWED_EXTENSIONS = {'docx'}

app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/freel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = LoginManager(app)

from freel import models, routes, forms, DocView

app.app_context().push()
db.create_all()
