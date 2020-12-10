from flask import Flask, Blueprint, render_template, request, redirect
from flask import current_app as app
from werkzeug.utils import secure_filename
from ..helpers import *
from ..config import S3_KEY, S3_SECRET, S3_BUCKET
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

        if email and password:
            db.execute(
                'SELECT id FROM user WHERE email = ? OR username = ?',
            (email,username,)  # and/or USERNAME ------------------
            ).fetchone() is not None:
                error = '{} is already registered.'.format(email)

        if error is None:
            db.execute(
                """
                INSERT INTO user (username, first_name, last_name, email, password)
                VALUES (?,?,?,?,?)
                """,
                # use JTW tokens instead ------------
                (username, first_name, last_name, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flask(error)

    # return render_template('auth/register.html')
