from flask_login import UserMixin

from freel import db, manager


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_type = db.Column(db.String(255), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    subscription_type = db.Column('subscription_id', db.ForeignKey("subscription.id"))


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(12), nullable=False)
    data = db.Column(db.DateTime(timezone=True))


class UserPreparation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey("user.id"))
    file_id = db.Column('file_id', db.ForeignKey("files.id"))


class UserTemplates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey("user.id"))
    template_id = db.Column('template_id', db.ForeignKey("files.id"))


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
