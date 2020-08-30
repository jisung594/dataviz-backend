from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from .helpers import *

app = Flask(__name__)
# -- in terminal --
# export FLASK_APP=main.py
# flask run

app.config.from_object("config")



@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if "input-file" not in request.files:
        return "Please upload a file."

    graph_name = request.form["graph-name"]
    x_axis = request.form["x-axis"]
    y_axis = request.form["y-axis"]
    file = request.files["input-file"]


    if file.filename == "":
        return "Please upload a file."


    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_to_s3(file, app.config["S3_BUCKET"], bucket_dir)

        return redirect('/')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
