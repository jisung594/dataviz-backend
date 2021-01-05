from flask import Flask, Blueprint, render_template, request, redirect
from flask import current_app as app
from werkzeug.utils import secure_filename
from ..helpers import *
from ..config import S3_BUCKET
# from flask_cors import CORS

# Blueprint config
upload_bp = Blueprint(
    'upload_bp', __name__
)

@upload_bp.route('/')
def index():
    return render_template('/index.html')

@upload_bp.route('/upload', methods=['POST'])
def upload():
    bucket_dir = request.form['bucketDir']
    format = request.form['format']
    input_file = request.files['inputFile']

    if input_file and allowed_file(input_file.filename):
        input_file.filename = secure_filename(input_file.filename)
        # output = upload_to_s3(input_file, app.config['S3_BUCKET'], bucket_dir)
        output = upload_to_s3(input_file, S3_BUCKET, bucket_dir)
        return str(output)
    else:
        print("Check if 'input_file' is valid or the file name passes 'allowed_file' func")
        return redirect('/')
