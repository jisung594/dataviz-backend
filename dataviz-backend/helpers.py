import boto3, botocore
from .config import S3_KEY, S3_SECRET, S3_BUCKET
from botocore.config import Config
# from .__init__ import app
import pymsgbox


ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json', 'xls', 'jpg', 'jpeg', 'png', 'pdf'])

def allowed_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_EXTENSIONS


s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_to_s3(file, bucket, bucket_dir, acl='private'):
    try:
        s3.upload_fileobj(
            file,
            bucket,
            "{}/{}".format(bucket_dir,file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    # pymsgbox.alert("Uploaded to {}/{}/{}".format(app.config["S3_LOCATION"], bucket_dir, file.filename), "Success")
