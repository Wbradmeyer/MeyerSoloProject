from flask import Flask
app = Flask(__name__)
UPLOAD_FOLDER = 'flask_app\static\images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.secret_key = "The first rule of secret key is..." 
