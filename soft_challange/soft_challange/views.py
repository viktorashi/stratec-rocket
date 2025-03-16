from flask import request, redirect, url_for, render_template, flash
from soft_challange import app
from utils import get_escape_velocities, get_escape_time_distance, get_travel_data
import os


def file_present_valid(file_name) -> []:
    """
    :param file_name: The name of the file as defined in our front-end
    :return: list: fierst element if good reposnbe or not
    """


def save_file(file, new_name):
    """
    :param file: The file to be saved
    :param new_name: The name to be saved as
    :return: The path to the saved file
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    #ignore this warning lmao
    request.files[file].save(filepath)
    return filepath


def proccess_planet_and_rocket_data() -> [[dict], dict]:
    """
    Just keeping it DRY
    :return:
    """

    rocket_data_filepath = save_file('rocket_data_file', 'rocket_data_file.txt')
    planteray_data_filepath = save_file('planetary_data_file', 'planetary_data_file.txt')
    # process the file and compute data
    with open(planteray_data_filepath, 'r') as f:
        planetary_data = f.read()
    with open(rocket_data_filepath, 'r') as f:
        rocket_data = f.read()
    planets, rocket = get_escape_time_distance(planetary_data, rocket_data)
    return planets, rocket


@app.get('/')
def home():
    return render_template("home.html")


@app.post('/upload')
def upload():
    ## asta formeaza gen guardul
    ### daca vrem sa aflam chestii desrpe sistemul solar ne trebuie toate alea de dinainte,
    ### daca vrem doar despre ce face reckta noastra cand decoleaza ne trebuie alea planetare,
    ### si alea planetare sunt singurele gen 'indenpendente' sa zic asa

    if request.files['solar_system_data_file'].filename != '':
        if not (request.files['planetary_data_file'] or request.files['rocket_data_file']):
            flash('We need both planetary and rocket data for this!')
            return redirect(url_for('home'))

        planets, rocket = proccess_planet_and_rocket_data()
        save_file('solar_system_data_file', 'solar_system_data_file.txt')

        return render_template('result.html', planets=planets, rocket=rocket, travel_data=True)

    if request.files['rocket_data_file'].filename != '':
        if not request.files['planetary_data_file']:
            flash('We need planetary data for this as well!')
            return redirect(url_for('home'))

        planets, rocket = proccess_planet_and_rocket_data()

        return render_template('result.html', planets=planets, rocket=rocket)

    if request.files['planetary_data_file'].filename != '':
        if request.files['planetary_data_file'].filename == '':
            flash('We need at least planetary data for this!')
            return redirect(url_for('home'))

        planteray_data_filepath = save_file('planetary_data_file')
        # process the file and compute data
        with open(planteray_data_filepath, 'r') as f:
            data = f.read()
        computed_data = get_escape_velocities(data)
        return render_template('result.html', planets=computed_data)
    else:
        flash('Cmonnn upload *somethinggg*!!')
        return redirect(url_for('home'))


@app.post('/travel')
def travel():
    # this will be a form with two select fields containing planet names their names are from_planet and to_planet, first check if they are different and giev a flash if not
    from_planet = request.form['from_planet']
    to_planet = request.form['to_planet']

    if from_planet == to_planet:
        flash('These are the same planets, dummyy')
        return redirect(url_for('upload'))

    solar_system_data = os.path.join(app.config['UPLOAD_FOLDER'], 'solar_system_data_file.txt')

    with open(solar_system_data, 'r') as f:
        solar_system_data = f.read()

    planetary_data_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'planetary_data_file.txt')
    rocket_data_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'rocket_data_file.txt')

    # process the file and compute data
    with open(planetary_data_filepath, 'r') as f:
        planetary_data = f.read()
    with open(rocket_data_filepath, 'r') as f:
        rocket_data = f.read()
    planets, rocket = get_escape_time_distance(planetary_data, rocket_data)

    travel_results = get_travel_data(solar_system_data, planets, rocket, from_planet, to_planet)

    return render_template("travel.html", travel=travel_results, fromPlanet = from_planet, toPlanet = to_planet)
