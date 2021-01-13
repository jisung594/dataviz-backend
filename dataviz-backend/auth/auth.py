from flask import Flask, Blueprint, flash, request, redirect, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from ..helpers import *
from ..config import S3_KEY, S3_SECRET, S3_BUCKET
from ..db import get_db
from flask_cors import CORS
import flask_praetorian


# Blueprint config
auth_bp = Blueprint(
    'auth_bp', __name__
)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        res = None

        # ****** EXISTING USER ******
        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            res = {'status':'existing', 'id':row[0]}


        # ****** NEW USER ******
        if res is None:
            db.execute(
                """
                INSERT OR IGNORE INTO user (first_name, last_name, email, password)
                VALUES (?,?,?,?)
                """,
                # use JTW tokens as well ------------
                (first_name, last_name, email, generate_password_hash(password))
            )
            db.commit()
            row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            res = {
                'status':'new',
                'user': {
                    'id': row[0],
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                }
            }

        # flash(status)
        return res


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        guard = flask_praetorian.Praetorian()  # ******************************

        res = None

        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            # ****** CHECK PASSWORD ******
            # row = db.execute('SELECT id FROM user WHERE email = ?', (email)).fetchall()

            user = guard.authenticate(email,password)
            res = {'access_token': guard.encode_jwt_token(user)}

        return res
