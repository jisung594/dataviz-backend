import os
# from flask import current_app as app

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
S3_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET = os.environ.get('S3_SECRET_ACCESS_KEY')
S3_LOCATION = 'https://{}.s3.us-east-1.amazonaws.com'.format(S3_BUCKET)

# DATABASE = os.path.join(app.instance_path, 'dataviz-backend.db')
DATABASE = './dataviz-backend/dataviz-backend.db'

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000
