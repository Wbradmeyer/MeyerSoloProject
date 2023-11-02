from flask import Flask
app = Flask(__name__)
UPLOAD_FOLDER = 'flask_app\static\images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "The first rule of secret key is..." 

# The secret key is needed to run session
# This is one thing that would usually be kept in your git ignore, along with API keys