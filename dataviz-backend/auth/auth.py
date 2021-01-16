from flask import Flask, Blueprint, flash, request, redirect, session
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from ..helpers import *
from ..config import S3_KEY, S3_SECRET, S3_BUCKET
from ..db import get_db
from flask_cors import CORS
# import flask_praetorian

from flask_sqlalchemy import SQLAlchemy


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

        # ***************** EXISTING USER *****************
        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            res = {'status':'existing', 'id':row[0]}


        # ***************** NEW USER *****************
        if res is None:
            db.execute(
                """
                INSERT OR IGNORE INTO user (first_name, last_name, email, password)
                VALUES (?,?,?,?)
                """,
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

            # ---------------------------------------------
            session.clear()
            session['user_id'] = user[row[0]]
            # ---------------------------------------------

        return res


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    # Log in user and create session
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        # guard = flask_praetorian.Praetorian()  # ******************************

        res = None

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            res = {
                'error': 'Username or password is incorrect.',
                'user': None
            }

        if res is None:
            session.clear()
            session['user_id'] = user['id']

            res = {
                'error': 'None',
                'user': {
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'email': user['email']
                }
            }

        print(session)
        return res

    # Check if user is logged in
    if request.method == 'GET':
        if session.get('user_id') is None:
            return {'user_id': None}

        return {'user_id': session['user_id']}

        print(session)


@auth_bp.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        # session.clear()
        session.pop('user_id', None)
        print(session)
        return {'user_id': None}
