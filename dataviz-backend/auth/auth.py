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
        error = None

        if db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
                error = '{} is already registered.'.format(email)

        if error is None:
            db.execute(
                """
                INSERT OR IGNORE INTO user (username, first_name, last_name, email, password)
                VALUES (?,?,?,?,?)
                """,
                # use JTW tokens instead ------------
                (username, first_name, last_name, email, generate_password_hash(password))
            )
            db.commit()

        # flash(error)

    return error
