import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import boto3
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO USER')

access_key_id = os.getenv('AWSAccessKeyId')
secret_key = os.getenv('AWSSecretKey')


s3 = boto3.client('s3',
                    aws_access_key_id = access_key_id,
                    aws_secret_access_key = secret_key)


BUCKET_NAME = 'aws-python-upload'
UPLOAD_FOLDER = './client/uploads'

app = Flask(__name__)
CORS(app, expose_headers='Authorization', resources={r"/upload/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to the local upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    s3.upload_file(Bucket = BUCKET_NAME,
        Filename = destination,
        Key = filename)
    session['uploadFilePath']=destination
    msg = 'Upload Successful'
    response="Whatever you wish too return"

    return response, msg 

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)


