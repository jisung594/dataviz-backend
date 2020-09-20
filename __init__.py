from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from .helpers import *
from flask_cors import CORS

app = Flask(__name__)
# -- in terminal --
# source venv/bin/activate
# export FLASK_APP=__init__.py
# python -m flask run

app.config.from_object("config")
CORS(app)


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/upload", methods=["POST"])
def upload():
    bucket_dir = request.form["bucketDir"]
    format = request.form["format"]
    input_file = request.files["inputFile"]

    if input_file and allowed_file(input_file.filename):
        input_file.filename = secure_filename(input_file.filename)
        output = upload_to_s3(input_file, app.config["S3_BUCKET"], bucket_dir)

        return redirect("/")
    else:
        return redirect("/")



# def upload_file():
#     if "input-file" not in request.files:
#         return "Please upload a file."
#
#     graph_name = request.form["graph-name"]
#     x_axis = request.form["x-axis"]
#     y_axis = request.form["y-axis"]
#     file = request.files["input-file"]
#
#
#     if file.filename == "":
#         return "Please upload a file."
#
#
#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output = upload_to_s3(file, app.config["S3_BUCKET"], bucket_dir)
#
#         return redirect('/')
#     else:
#         return redirect('/')




if __name__ == "__main__":
    app.run(Debug=True)
