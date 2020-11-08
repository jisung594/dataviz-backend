from flask import Flask
from flask_cors import CORS
import os

# -- in terminal --
# source venv/bin/activate
# export FLASK_APP=__init__.py
# export FLASK_ENV=development
# python -m flask run


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_pyfile("config.py")

    with app.app_context():
        from .upload import upload
        app.register_blueprint(upload.upload_bp)


    # register the database commands
    from . import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app.run(Debug=True)
