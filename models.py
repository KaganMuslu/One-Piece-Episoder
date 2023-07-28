from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class OPE_User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    list_setting = db.Column(db.Integer, default=0)
    last_episode = db.Column(db.Integer, default=0)
    last_episode_date = db.Column(db.DateTime(timezone=True), default=func.now())


class OPE_Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    title = db.Column(db.String, unique=True)


class OPE_Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String)
    message_date = db.Column(db.DateTime(timezone=True), default=func.now())
