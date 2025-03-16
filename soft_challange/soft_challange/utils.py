from math import sqrt


def get_escape_velocities(data: str) -> [dict]:
    planets = parse_planets(data)

    for planet in planets:
        planet['escape_velocity'] = calculate_escape_velocity(planet['mass'], planet['diameter'] / 2)
        print(planet)

    return planets


def get_escape_time_distance(planetary_data: str, rocket_data: str) -> [dict]:
    """
    :param planetary_data: string with data about planets
    :param rocket_data: string with data about rockets
    :return: the planets ( now with escape_velocity, escape_time and escape_distance data) and rocket_data dicts
    """
    planets = parse_planets(planetary_data)
    rocket_data = parse_rocket(rocket_data)

    for planet in planets:
        # we first need the scape velocities
        planet['escape_velocity'] = calculate_escape_velocity(planet['mass'], planet['diameter'] / 2)
        planet['escape_time'] = calculate_escape_time(planet, rocket_data)
        planet['escape_distance'] = calculate_escape_distance(rocket_data['acceleration'] * rocket_data['engine_count'],
                                                              planet['escape_time'])
        print(planet)

    return planets, rocket_data


def parse_travel(travel_data: str, planetary_data: [dict]) -> [dict]:
    """
    Obtains list of planets but with orbital radii now

    :param travel_data: file of the form
        Mercury: period = 88 days, orbital radius = 0.39 AU
        Venus: period = 225 days, orbital radius = 0.72 AU
        Earth: period = 365 days, orbital radius = 1 AU
        Mars: period = 687 days, orbital radius = 1.52 AU
        Jupiter: period = 4329 days, orbital radius = 5.2 AU
        Saturn: period = 10753 days, orbital radius = 9.54 AU
        Uranus: period = 30660 days, orbital radius = 19.18 AU
        Neptune: period = 60148 days, orbital radius = 30.06 AU
        Pluto: period = 90560 days, orbital radius = 39.6 AU

    :param planetary_data:
    :return: list of planets but with orbital radii now
    """

    for planet in planetary_data:
        for line in travel_data.split('\n'):
            if planet['name'] in line:
                planet['orbital_radius'] = float(line.split('=')[2].split(' ')[1])
                break

    return planetary_data


def get_travel_data(travel_data: str, planetary_data: [dict], rocket_data: dict, from_planet: str,
                    to_planet: str) -> dict:
    """
    :param travel_data: string from traveel.txt of the form:
        Mercury: period = 88 days, orbital radius = 0.39 AU
        Venus: period = 225 days, orbital radius = 0.72 AU
        Earth: period = 365 days, orbital radius = 1 AU
        Mars: period = 687 days, orbital radius = 1.52 AU
        Jupiter: period = 4329 days, orbital radius = 5.2 AU
        Saturn: period = 10753 days, orbital radius = 9.54 AU
        Uranus: period = 30660 days, orbital radius = 19.18 AU
        Neptune: period = 60148 days, orbital radius = 30.06 AU
        Pluto: period = 90560 days, orbital radius = 39.6 AU

    :param planetary_data: returned by get_escape_time_distance
    :param rocket_data: returned by get_escape_time_distance
    :param from_planet: from the form
    :param to_planet:  from the form
    :return: the 6 requirements of the problem statement in a dict

     // take the ecape velocities of the two planets, and set the max of them to be the cruising velocity
    'escape_time' 1. the time it takes to reach the cruising velocity from the start planet : planetary_data['max_velocity_planet']['escape_time']
    'escape_distance' 2. the distance from the surface when it reaches it :  planetary_data['max_velocity_planet']['escape_distance']
    'cruise_time' 3. Cruise time : ( distance_between_planets_centers - 2 * escape_distance - radius_from_planet -radius_to_planet ) / cruising_velocity
    'escape_distance' 4. Distance at which it starts deccelarting (from planet's surface) : SAME AS 2. !! ( nu inteleg eu ceva? gen e intrebare capana pusa inca o data?)
    'escape_time' 5. Time to deccelerate to 0 : SAME AS 1. !!!!1 (again, sunt eu prost?)
    'total_travel_time' 6. Total travel time : ( distance_between_planets_centers - radius_from_planet - radius_to_planet ) / cruising_velocity
    # ( in days, hours, minutes, seconds)

    """

    planets = parse_travel(travel_data, planetary_data)

    from_planet_data = -1
    to_planet_data = -1
    travel_results = {}

    for planet in planets:
        if planet['name'] == from_planet:
            from_planet_data = planet
        elif planet['name'] == to_planet:
            to_planet_data = planet
        elif from_planet_data != -1 and to_planet_data != -1:
            break

    if from_planet_data['escape_velocity'] > to_planet_data['escape_velocity']:
        cruising_velocity = from_planet_data['escape_velocity']
        escape_distanace = from_planet_data['escape_distance']
        escape_time = from_planet_data['escape_time']
    else:
        cruising_velocity = to_planet_data['escape_velocity']
        escape_distanace = to_planet_data['escape_distance']
        escape_time = to_planet_data['escape_time']

    travel_results['escape_time'] = escape_time
    travel_results['escape_distance'] = escape_distanace

    # in AU's
    distance_between_planet_centers = abs(from_planet_data['orbital_radius'] - to_planet_data['orbital_radius'])

    AU = 149597870.7 * (10 ** 3)  # 1 AU in meters

    distance_between_planet_centers = distance_between_planet_centers * AU

    # long boi
    travel_results['cruise_time'] = calculate_cruise_time(distance_between_planet_centers, escape_distanace,
                                                          from_planet_data['diameter'] * (10 ** 3) / 2,
                                                          to_planet_data['diameter'] * (10 ** 3) / 2, cruising_velocity)

    #actually unreadable
    travel_results['total_travel_time'] = ((distance_between_planet_centers -
                                            from_planet_data['diameter'] * (10 ** 3) / 2 - to_planet_data[
                                                'diameter'] * (10 ** 3) / 2)
                                           / cruising_velocity)

    return travel_results


def calculate_escape_velocity(mass, radius) -> float:
    """
    :param mass: of the planet in kg
    :param radius: of the planet in km (needs converted to SI)
    :return: its escape velocity in m/s
    """
    G = 6.67430 * (10 ** -11)  # Newton’s gravitational constant
    return sqrt(2 * G * mass / (radius * (10 ** 3)))


def calculate_escape_time(planet: dict, rocket_data: dict) -> float:
    """
    :param planet: Dict with data about the planet of the type {"name": "Earth", "diameter": 12800, "mass": 6 * (10 ** 24)}
    :param rocket_data: dict with no. of engines and each engine's acceleration {"engine_count": 4, "acceleration": 10}
    :return: escape time in seconds : velocity / ( engine_count * acceleration_per_engine)
    """
    return planet['escape_velocity'] / (rocket_data['engine_count'] * rocket_data['acceleration'])


def calculate_escape_distance(acceleration, escape_time) -> float:
    return (acceleration * escape_time ** 2) / 2


def calculate_cruise_time(distance_between_planets_centers, escape_distance, radius_from_planet, radius_to_planet,
                          cruising_velocity) -> float:
    return (
            distance_between_planets_centers - 2 * escape_distance - radius_from_planet - radius_to_planet) / cruising_velocity


def parse_rocket(file_data: str) -> dict:
    """
    :param file_data: Contents of the form:
    Number of rocket engines: 4
    Acceleration per engine: 10 m/s^2

    :return: dict of the form {"engine_count": 4, "acceleration": 10}
    """

    rocket = {}
    # there's only two lines lmao
    file_lines = file_data.split('\n')[:-1]
    [no_engines, acceleration_per_engine] = file_lines

    no_engines = int(no_engines.split(': ')[1])
    acceleration_per_engine = float(acceleration_per_engine.split(': ')[1].split(' ')[0])

    rocket["engine_count"] = no_engines
    rocket["acceleration"] = acceleration_per_engine

    return rocket


def parse_planets(file_data: str) -> [dict]:
    """
    # e gen lista din fisier, exemplu:
# Mercury: diameter = 4900 km, mass = 0.06 Earths
# Venus: diameter = 12100 km, mass = 0.82 Earths
# Earth: diameter = 12800 km, mass = 6 * 10^24 kg
# Mars: diameter = 5800 km, mass = 0.11 Earths
# Jupiter: diameter = 142800 km, mass = 318 Earths
# Saturn: diameter = 120000 km, mass = 95 Earths
# Uranus: diameter = 52400 km, mass = 15 Earths
# Neptune: diameter = 48400 km, mass = 17 Earths
# Pluto: diameter = 2450 km, mass = 0.002 Earths
    :param file_data: string cu date cum sunt scirse sus
    :return: lista cu dicturi de forma

    { "name" :planeta,
    "diameter": diametru,
    "mass": masa ( calculata in kg dupa ce s-a aflat care e aia a pamantului si dupa luata ce proportie e aia din masa pamantukui)
    }
    """

    print(file_data)
    earth_mass = -1
    planets = []
    for line in file_data.split('\n'):
        if line != '':
            eq_split = line.split('=')

            planet_name = line.split(':')[0]
            # in km's si tine minte ca vrem SI units
            diameter = int(eq_split[1].split(',')[0].split(' ')[1])
            mass = eq_split[2]

            if 'kg' == mass[-2:]:
                # kg (cam multe)
                mass = 6 * (10 ** 24)  # a bit cheap but does the job
                earth_mass = mass
            # daca nu e pamantul dar e dupa ce s-a gasti pamantul
            elif earth_mass != -1:
                earths_masses = mass.split(' ')[1]
                mass = earth_mass * float(earths_masses)
            # the ones before earth came up
            else:
                mass = float(mass.split(' ')[1])

            planets.append({
                "name": planet_name,
                "diameter": diameter,
                "mass": mass
            })

    for planet in planets:
        if planet['name'] != 'Earth':
            planet["mass"] = planet["mass"] * earth_mass
        else:
            break

    return planets
