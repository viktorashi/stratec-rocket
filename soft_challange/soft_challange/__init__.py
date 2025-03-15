import os
from flask import Flask

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

import soft_challange.views

if __name__ == '__main__':
    app.run(debug=True)