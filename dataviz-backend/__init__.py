from flask import Flask
from flask_cors import CORS
import os
from flask_login import LoginManager

# -- in terminal --------------------------------------
# source venv/bin/activate && export FLASK_APP=__init__.py && export FLASK_ENV=development
# flask run
# -----------------------------------------------------
# source venv/bin/activate
# export FLASK_APP=__init__.py && export FLASK_ENV=development
# flask run ( OR python -m flask run )


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_pyfile("config.py")

    login_manager = LoginManager(app)     #----------------------
    login_manager.init_app(app)   #----------------------

    with app.app_context():
        from .auth import auth
        app.register_blueprint(auth.auth_bp)
        from .upload import upload
        app.register_blueprint(upload.upload_bp)
        from .retrieve import retrieve
        app.register_blueprint(retrieve.retrieve_bp)


    # register the database commands
    from . import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app.run(Debug=True)
