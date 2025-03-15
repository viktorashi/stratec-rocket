from flask import request, redirect, url_for, render_template, flash
from soft_challange import app
from utils import get_escape_velocities, get_escape_times
import os


@app.route('/')
def home():
    return render_template("home.html")

def file_present_valid(file_name)-> []:
    """
    :param file_name: The name of the file as defined in our front-end
    :return: list: fierst element if good reposnbe or not 
    """

def save_file(file):
    """
    :param file: The file to be saved
    :return: The path to the saved file
    """
    filename = request.files[file].filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    request.files[file].save(filepath)
    return filepath

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'planetary_data_file' not in request.files:
        flash('We need at least planetary data for this!')
        return redirect(url_for('home'))

    if request.files['planetary_data_file'].filename == '':
        flash("No selected file ( I think, it doesn't really make sense)")
        return redirect(url_for('home'))

    planteray_data_filepath = save_file('planetary_data_file')

    #it's just planetary data so we need to compute the escape velocity
    if not request.files['rocket_data_file']:
        # process the file and compute data
        with open(planteray_data_filepath, 'r') as f:
            data = f.read()
        computed_data = get_escape_velocities(data)
        return render_template('result.html', planets=computed_data)
    # adica sunt ambele, ca s-a verificat inaitne cad aca exista planeetary data
    else:

        rocket_data_filepath = save_file('rocket_data_file')
        # process the file and compute data
        with open(planteray_data_filepath, 'r') as f:
            planetary_data = f.read()
        with open(rocket_data_filepath, 'r') as f:
            rocket_data = f.read()
        planets, rocket = get_escape_times(planetary_data, rocket_data)
        return render_template('result.html', planets=planets, rocket=rocket)


