from flask import request, redirect, url_for, render_template, flash
from soft_challange import app
from utils import get_escape_velocities
import os


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'planetary_data_file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    file = request.files['planetary_data_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    if file:
        #TODO poate-i faci mai incolo secure la filename
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        request.files['planetary_data_file'].save(filepath)
        # Process the file and compute data
        with open(filepath, 'r') as f:
            data = f.read()
        computed_data = get_escape_velocities(data)
        return render_template('result.html', data=computed_data)
    else:
        flash('Invalid file type')
        return redirect(url_for('home'))


