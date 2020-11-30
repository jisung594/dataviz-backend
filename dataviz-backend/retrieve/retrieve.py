from flask import Flask, Blueprint, request, redirect
from flask import current_app as app
from ..helpers import *
from ..config import S3_BUCKET


# Blueprint config
retrieve_bp = Blueprint(
    'retrieve_bp', __name__
)


@retrieve_bp.route('/list_files', methods=['GET'])
def list_files():
    bucket_dir = 'Jon'
    # above --> designate a separate directory for users
    # use the one above as a placeholder

    output = read_s3_dir(S3_BUCKET, bucket_dir)
    return output


@retrieve_bp.route('/read_csv', methods=['GET', 'POST'])
def read():
    bucket_dir = 'Jon'
    # above --> designate a separate directory for users
    # use the one above as a placeholder

    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']

    output = read_csv_s3(S3_BUCKET, bucket_dir, x_axis, y_axis)
    return str(output)
