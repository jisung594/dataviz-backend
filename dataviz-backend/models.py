from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import relationship
from flask_appbuilder import Model


class User(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return self.email
