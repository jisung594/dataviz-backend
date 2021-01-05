from flask import Flask, Blueprint, flash, request, redirect, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from ..helpers import *
from ..config import S3_KEY, S3_SECRET, S3_BUCKET
from ..db import get_db
from flask_cors import CORS

# Blueprint config
auth_bp = Blueprint(
    'auth_bp', __name__
)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        # status = None
        res = None

        # ****** EXISTING USER ******
        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            res = {'status':'existing', 'id':row[0]}

        # if db.execute(
        #     'SELECT id FROM user WHERE email = ?', (email,)
        # ).fetchone() is not None:
        #         status = str(db.execute(
        #         'SELECT id FROM user WHERE email = ?', (email,)
        #         ).fetchone())
        #         # status = 'false'


        # ****** NEW USER ******
        if res is None:
            db.execute(
                """
                INSERT OR IGNORE INTO user (username, first_name, last_name, email, password)
                VALUES (?,?,?,?,?)
                """,
                # use JTW tokens as well ------------
                (username, first_name, last_name, email, generate_password_hash(password))
            )
            db.commit()
            row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            res = {'status':'new', 'id':row[0]}
            # status = 'true'

        # ------------------------------------------------
        # -- when the email is ALREADY registered, it correctly sends back response
        #    (HOWEVER, even unregistered emails sent to frontend as ALREADY REGISTERED)
        # -- when the email is NOT registered
        # ------------------------------------------------


        # flash(status)
        return res
