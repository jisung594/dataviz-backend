from flask_login import UserMixin
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy import relationship
# from flask_appbuilder import Model
from .db import get_db
# from flask import current_app as app
# from flask_sqlalchemy import SQLAlchemy


# # db = get_db()  # AttributeError: 'sqlite3.Connection' object has no attribute 'Model'
# app.config['SQLALCHEMY_DATABASE_URI'] = get_db()
# db = SQLAlchemy(app)


db = get_db()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(20), nullable=False)
#     last_name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(40), unique=True, nullable=False)
#     password = db.Column(db.String(20), nullable=False)
#
#     def __repr__(self):
#         return self.email
