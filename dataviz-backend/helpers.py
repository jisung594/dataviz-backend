import boto3, botocore
from .config import S3_KEY, S3_SECRET, S3_BUCKET
from botocore.config import Config
# from .__init__ import app
import pymsgbox
import codecs
import csv


ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json', 'xls', 'jpg', 'jpeg', 'png', 'pdf'])

def allowed_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_EXTENSIONS


s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

# UPLOAD ------------------------------
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
        print("Error: ", e)
        return e

    # pymsgbox.alert("Uploaded to {}/{}/{}".format(app.config["S3_LOCATION"], bucket_dir, file.filename), "Success")



# RETRIEVE ------------------------------
def read_s3_dir(bucket, bucket_dir, acl='private'):
    try:
        files = {
            'directory': bucket_dir,
            'files': []
        }

        # *** 'bucket_dir' should be a logged-in username ***
        for key in s3.list_objects(Bucket=bucket, Prefix=bucket_dir)['Contents']:
            file_name = key['Key'].split('/')[1]
            if file_name != '':
                files['files'].append(file_name)
                print(file_name)
            else:
                print('*** placeholder for bucket directory ***')

        return files

    except Exception as e:
        print("Error: ", e)
        return e


def read_csv_s3(bucket, bucket_dir, x_axis, y_axis, acl='private'):
    try:
        data = s3.get_object(
            Bucket=bucket,
            # Prefix=bucket_dir,
            Key='Jon/new-york-history.csv'
        )

        col_vals = []
        for row in csv.DictReader(codecs.getreader('utf-8')(data['Body'])):
            # *** pass in column name as argument in read_csv_3 func ***
            # print(row[column])
            # print(row['death'])
            col_vals.append({
                x_axis: row[x_axis],
                y_axis: row[y_axis]
            })

        return col_vals[:3]
        # return col_vals

    except Exception as e:
        print("Error: ", e)
        return e
# --------------------------------------------
