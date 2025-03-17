from math import sqrt, cos, sin
import matplotlib
import matplotlib.pyplot as plt
from numpy import ndarray

# backendu gen sa poata sa mearga inafara de main thread
matplotlib.use('agg')
import numpy as np

AU = 149597870.7 * (10 ** 3)  # 1 AU in meters


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


def parse_solar_system_data(travel_data: str, planetary_data: [dict]) -> [dict]:
    """
    Obtains list of planets but with orbital radii (in AU) and periods (in days) now

    planet['orbital_radius']
    planet['period']

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
                planet['period'] = float(line.split('=')[1].split(' ')[1])
                break

    return planetary_data


def get_stupid_travel_data(planets: [dict], from_planet: str,
                           to_planet: str) -> dict:
    """
    Simple version (stage 5)
    :param planets: returned by proccess_solar_system_data
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

    distance_between_planet_centers = distance_between_planet_centers * AU

    # long boi
    travel_results['cruise_time'] = calculate_cruise_time(distance_between_planet_centers, escape_distanace,
                                                          from_planet_data['diameter'] * (10 ** 3) / 2,
                                                          to_planet_data['diameter'] * (10 ** 3) / 2, cruising_velocity)

    # actually unreadable
    travel_results['total_travel_time'] = ((distance_between_planet_centers -
                                            from_planet_data['diameter'] * (10 ** 3) / 2 - to_planet_data[
                                                'diameter'] * (10 ** 3) / 2)
                                           / cruising_velocity)

    return travel_results


"""
     merg in fiecare zi
        fa un dict care se updateaza in fiecare zi cu unghiul la care e fiecare planeta de pe traiectoriia mea, unde cheia e raza orbitala la planeta ca oricum e unica
            { orbital_radius: angular_position, ... } 

     e distanta mai mica decat ce am vazut inainte?
        la distanta nu e greu, stiu unghiurile lor fac unghiu dintre ele: 

        unghi = abs ( unghi1 - unghi2 )
        d^2 = r1^2 + r2^2 - 2 * r1 * r2 * cos(unghi)

     daca da, ma uit: unde sunt astea fiecare, le intersectez in ziua aia? (inafara de alea de unde plec si unde ma duc)

        aici mai greut un pic deci:
            daca fac coordonate carteziane pt centrul planetei de la care plec si unde ma duc pot sa parametrizsez traiectoria:
                lambda * (x1, y1) + (1 - lambda) * (x2, y2) = (x, y)
            cercul orbitei planetei (centrat la zero unde e soarele):
                x^2 + y^2 = r^2

            daca le intersectez imi da lambdaurile (dupa 3 pagini de calcule):

            for r in planets_orbital_radii:
                a = x1^2 + y1^2 - 2*x1*x2 - 2*y1*y2 + y2^2 + x2^2
                b = 2 * ( x1*x2 + y1*y2 - x2^2 - y2^2 )
                c = x2^2 + y2^2 - r^2
                delta = b^2 - 4*a*c

                if delta < 0:
                    (GOOD) nu se intersecteaza, so don't even worry. poti sa treci la urmatoru 
                elif este traiectoria mea? or e traiectoria la aia unde ma duc?:
                    (GOOD) la, fel nu ma intereseaza 
                elif delta == 0:
                    lambda =  -b / 2*a

                    inclocuiesc dupaia inapoi lambda in
                    lambda * (x1, y1) + (1 - lambda) * (x2, y2) = (xintersect, yintersect)
                    sa vad ce punct e acolo la intersectie 
                    si vad daca distanta de la punctul asta la centrul planetei de raza orbitala r e mai mica decat raza planetei

                    if sqrt( (xintersect - xplaneta)^2 + (yintersect - yplaneta)^2 ) > rplaneta:
                        (GOOD) pentru toate cu care se intersecteaza 
                    else:
                        (BAD) taie TATTTOTTT ce-ai fct pana acm, treci la urmatoarea zi


                #sunt 2 intersectii la care tre sa ma uit
                else delta > 0:        
                lambda1 =  ( -b + sqrt(delta) ) / 2*a
                lambda2 =  ( -b - sqrt(delta) ) / 2*a

                for lambda in [lambda1, lambda2]:
                    # sa vad ce punct e acolo la intersectie 
                    lambda * (x1, y1) + (1 - lambda) * (x2, y2) = (xintersect, yintersect)

                    if sqrt( (xintersect - xplaneta)^2 + (yintersect - yplaneta)^2 ) > rplaneta:
                        (GOOD) pentru toate cu care se intersecteaza 
                    else:
                        (BAD) taie TATTTOTTT ce-ai fct pana acm, treci la urmatoarea zi


    salveaza ultima zi in care ai putut sa treci de la unu la altu macar (prbabil nu e chiar cea mai optima, in cazu in care n-ar fi fost alte planete, dar ai incercat si tu) 
"""


def plot_planets(angles: list[float], planets_radii: list[float], orbit_radii: int | float | list[float] | ndarray,
                 planet_colors: list[str] | list[float], planet_names: list[str], planet1_name: str,
                 planet2_name: str,
                 saveto_filename: str):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    planet_positions = {}

    for i, (angle, radius, color, name) in enumerate(zip(angles, planets_radii, planet_colors, planet_names)):
        # Each planet's orbit radius
        if type(orbit_radii) == int or type(orbit_radii) == float:
            orbit_radius = (i + 1) * orbit_radii
        elif type(orbit_radii) == list or type(orbit_radii) == ndarray:
            orbit_radius = orbit_radii[i]
        else:
            raise ValueError(
                "Invalid type for orbit_radii: {} ; but expected int, float or list[float]".format(type(orbit_radii)))

        # Draw the orbit as a circle
        theta = np.linspace(0, 2 * np.pi, 200)
        x_orbit = orbit_radius * np.cos(theta)
        y_orbit = orbit_radius * np.sin(theta)
        ax.plot(x_orbit, y_orbit, color='gray', linestyle='--')

        # Convert the angle from degrees to radians
        angle_rad = np.deg2rad(angle)

        # Compute the planet's position on the orbit
        x_planet = orbit_radius * np.cos(angle_rad)
        y_planet = orbit_radius * np.sin(angle_rad)

        # Store the position
        planet_positions[name] = (x_planet, y_planet)

        # Plot the planet with the specified radius
        planet_circle = plt.Circle((x_planet, y_planet), radius, color=color, fill=True)
        ax.add_patch(planet_circle)
        ax.text(x_planet, y_planet, f' {name}', fontsize=10, verticalalignment='bottom')

    # Draw a line between the selected planets
    if planet1_name in planet_positions and planet2_name in planet_positions:
        x1, y1 = planet_positions[planet1_name]
        x2, y2 = planet_positions[planet2_name]
        ax.plot([x1, x2], [y1, y2], 'r-', linewidth=2, label=f"{planet1_name} ↔ {planet2_name}")

    # Mark the center (could be the star)
    ax.plot(0, 0, 'yo', markersize=12, label='Center')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    plt.savefig(saveto_filename)


def get_medium_travel_data(planets: [dict], from_planet: str, to_planet: str) -> dict | bool:
    """
    Stage 5: Gets the same results as stage 3 but with

    1. optimal_transfer_window in days or years whatever that shows
    the day in which you start the travel starting from t0

    2. the angular positions of the planets on that day

    t0 will now be 100 years from when they were aligned

    :param planets:
    :param from_planet:
    :param to_planet:
    :return: the 6 requirements of the problem statement in a dict | or False if it's impossible and your constantly blocked by other planets
    """

    from_planet_data = -1
    to_planet_data = -1

    for planet in planets:
        if planet['name'] == from_planet:
            from_planet_data = planet
        elif planet['name'] == to_planet:
            to_planet_data = planet
        elif from_planet_data != -1 and to_planet_data != -1:
            break

    t0 = 100 * 365  # 100 years
    min_distance = 9999999999999999999999999999999999999999999  # TODO stiu ca pot sa iau doar diametrul de la cel mai departe but idk this just simpler
    optimal_transfer_window_day = -1

    # in metrii
    r1 = from_planet_data['orbital_radius'] * AU
    r2 = to_planet_data['orbital_radius'] * AU

    # looks in the future for 10 years
    for day in range(365 * 10):
        angular_positions = get_angular_positions(planets, t0 + day)

        # angle between the two planets
        from_planet_angle = angular_positions[from_planet][0]
        to_planet_angle = angular_positions[to_planet][0]

        angle = abs(from_planet_angle - to_planet_angle)
        # straight line distance between the two planets
        distance = sqrt(r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * cos(angle))
        if distance < min_distance:
            crashes = False
            for planet_name in angular_positions:
                angular_position, orbit_radius, planet_radius = angular_positions[planet_name]
                orbit_radius = orbit_radius * AU  # in metrii
                if not (planet_name == from_planet or planet_name == to_planet):
                    # coordinates of the source and destination planets in cartesian
                    x1 = r1 * cos(from_planet_angle)
                    y1 = r1 * sin(from_planet_angle)
                    x2 = r2 * cos(to_planet_angle)
                    y2 = r2 * sin(to_planet_angle)

                    a = x1 ** 2 + y1 ** 2 - 2 * x1 * x2 - 2 * y1 * y2 + y2 ** 2 + x2 ** 2
                    b = 2 * (x1 * x2 + y1 * y2 - x2 ** 2 - y2 ** 2)
                    c = x2 ** 2 + y2 ** 2 - orbit_radius ** 2
                    delta = b ** 2 - 4 * a * c

                    # perfectt nu se interseteaza niciaeri (in universul vizibil cel putin, nu ne apucam de quaternioni acm)
                    if delta < 0:
                        pass

                    # se intersecteaza, dar tangent asa la un singur punct
                    elif delta == 0:
                        # nu pot sa scriu lambda ca e gen sintaxa in python lol
                        lamb = -b / 2 * a
                        # lambda * (x1, y1) + (1 - lambda) * (x2, y2) = (xintersect, yintersect)
                        [xintersect, yintersect] = [lamb * x1 + (1 - lamb) * x2, lamb * y1 + (1 - lamb) * y2]
                        xplaneta = orbit_radius * cos(angular_position)
                        yplaneta = orbit_radius * sin(angular_position)

                        if sqrt((xintersect - xplaneta) ** 2 + (yintersect - yplaneta) ** 2) <= planet_radius ** 2:
                            crashes = True
                            break

                    # delta > 0, 2 intersectii
                    else:
                        lamb1 = (-b + sqrt(delta)) / 2 * a
                        lamb2 = (-b - sqrt(delta)) / 2 * a

                        xplaneta = orbit_radius * cos(angular_position)
                        yplaneta = orbit_radius * sin(angular_position)

                        for lamb in [lamb1, lamb2]:
                            [xintersect, yintersect] = [lamb * x1 + (1 - lamb) * x2, lamb * y1 + (1 - lamb) * y2]

                            if sqrt((xintersect - xplaneta) ** 2 + (yintersect - yplaneta) ** 2) <= planet_radius ** 2:
                                crashes = True
                                break

                if crashes:
                    # uitate la urmatoarea zi
                    break

            if not crashes:
                min_distance = distance
                optimal_transfer_window_day = day

    if optimal_transfer_window_day == -1:
        return False

    # amu plecam la drum
    travel_results = {}

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

    travel_results['cruise_time'] = calculate_cruise_time(min_distance, escape_distanace,
                                                          from_planet_data['diameter'] * (10 ** 3) / 2,
                                                          to_planet_data['diameter'] * (10 ** 3) / 2, cruising_velocity)

    travel_results['total_travel_time'] = ((min_distance -
                                            from_planet_data['diameter'] * (10 ** 3) / 2 - to_planet_data[
                                                'diameter'] * (10 ** 3) / 2)
                                           / cruising_velocity)

    # ok astea sunt noi))
    travel_results['optimal_transfer_window'] = optimal_transfer_window_day
    travel_results['angular_positions'] = get_angular_positions(planets, t0 + optimal_transfer_window_day)

    planets_angles = [angle[0] for angle in travel_results['angular_positions'].values()]
    planets_names = [planet for planet in travel_results['angular_positions']]
    planets_colors = ['#1a1a1a', '#e6e6e6', '#2f6a69', '#993d00', '#b07f35', '#b08f36', '#5580aa', '#366896', '#fff1d5']
    max_planet_diameter = max([planet['diameter'] for planet in planets])
    planets_radii_proportional = [planet['diameter'] / max_planet_diameter for planet in planets]

    # TODO ai putea sa faci su cu orbitele alea reale da dupa nu se pream ai vede bine
    plot_planets(planets_angles, planets_radii_proportional, 1, planets_colors, planets_names,
                 from_planet, to_planet, 'static/planets.png')
    # this time accurately with the plante radii
    largest_orbit_radius = max([planet['orbital_radius'] for planet in planets])
    planets_proportional_orbit_radii = [planet['orbital_radius'] / largest_orbit_radius for planet in planets]
    planets_proportional_orbit_radii = np.array(planets_proportional_orbit_radii)

    plot_planets(planets_angles, planets_radii_proportional, planets_proportional_orbit_radii * 19, planets_colors,
                 planets_names,
                 from_planet, to_planet, 'static/planets-accurate.png')

    # I mean we need to see it as wel smr

    return travel_results


def get_smart_travel_data(planets: [dict], from_planet: str, to_planet: str, rocket: dict) -> dict | bool:
    """
    Stage 6: Gets the same results as stage 5 but with the planets now moving WHILE the rocket is also en route
    :param planets: returned by proccess_solar_system_data
    :param from_planet: user selected from form
    :param to_planet: user selected from form
    :param rocket: {"acceleration" : acc, "engine_count" : no_of_engines}
    :return:
    """

    """
    cand se uita daca se 
    as face gen asemanator numai ca acum cand aflu lambda de intersectie potentiala vad cati km a parscurs din distanta
    
    lambda = 0 - sfarsit de drum
    labda = 1 - inceput de drum
    """

    from_planet_data = -1
    to_planet_data = -1

    for planet in planets:
        if planet['name'] == from_planet:
            from_planet_data = planet
        elif planet['name'] == to_planet:
            to_planet_data = planet
        elif from_planet_data != -1 and to_planet_data != -1:
            break

    t0 = 100 * 365  # 100 years
    # minimum TOTAL distance
    min_distance = 9999999999999999999999999999999999999999999  # TODO stiu ca pot sa iau doar diametrul de la cel mai departe but idk
    optimal_transfer_window_day = -1
    optimal_cruising_time = -1

    if from_planet_data['escape_velocity'] > to_planet_data['escape_velocity']:
        cruising_velocity = from_planet_data['escape_velocity']
        escape_distanace = from_planet_data['escape_distance']
        escape_time = from_planet_data['escape_time']
    else:
        cruising_velocity = to_planet_data['escape_velocity']
        escape_distanace = to_planet_data['escape_distance']
        escape_time = to_planet_data['escape_time']

    # radii in meters
    r1 = from_planet_data['orbital_radius'] * AU
    r2 = to_planet_data['orbital_radius'] * AU
    destination_angular_velocity = 360 / to_planet_data['period']

    # ok re zolvat pt total trabvel time is dupa ne dam seama cat vine fiecare stage de travel
    from scipy.optimize import root_scalar

    for day in range(365 * 10):

        # nu-mi trebuie acum angluar positions, iau dupa ce vad la ce timp trebuie sa ma uit si fac
        # get_angular_positions(planets,t0 + day + travel_time_to_intersect)

        # faci functia de distanta in functie de cruise_time
        to_planet_init_angle = get_angular_position(to_planet_data['period'], t0 + day)
        from_planet_angle = get_angular_position(from_planet_data['period'], t0 + day)

        # Define the function to find T
        def equation(T, v, a, Rd, Rs, theta_d0, omega_d, theta_s):
            lhs = v * T - v ** 2 / a
            rhs = np.sqrt((Rd * np.cos(theta_d0 - omega_d * T) - Rs * np.cos(theta_s)) ** 2 +
                          (Rd * np.sin(theta_d0 - omega_d * T) - Rs * np.sin(theta_s)) ** 2)
            return lhs - rhs

        total_time_sol = root_scalar(equation, args=(
            cruising_velocity, rocket['acceleration'], r2, r1, to_planet_init_angle, destination_angular_velocity,
            from_planet_angle), bracket=[0, 99999999999])

        # Print the solution
        if total_time_sol.converged:
            print(f"Solution for T: {total_time_sol.root}")
        else:
            print("No solution found!")

        total_time_sol = total_time_sol.root
        cruising_time = total_time_sol - 2 * escape_time
        distance = cruising_velocity * cruising_time + 2 * escape_distanace
        to_planet_final_angle = get_angular_position(to_planet_data['period'], t0 + day + total_time_sol / 86400)

        if distance < min_distance:
            crashes = False

            # does it crash into any planets on its way?
            for planet in planets:
                planet_name = planet['name']
                orbit_radius = planet['orbital_radius'] * AU
                if not (planet_name == from_planet or planet_name == to_planet):
                    # coordinates of the source and destination planets in cartesian
                    x1 = r1 * cos(from_planet_angle)
                    y1 = r1 * sin(from_planet_angle)
                    x2 = r2 * cos(to_planet_final_angle)
                    y2 = r2 * sin(to_planet_final_angle)

                    a = x1 ** 2 + y1 ** 2 - 2 * x1 * x2 - 2 * y1 * y2 + y2 ** 2 + x2 ** 2
                    b = 2 * (x1 * x2 + y1 * y2 - x2 ** 2 - y2 ** 2)
                    c = x2 ** 2 + y2 ** 2 - orbit_radius ** 2
                    delta = b ** 2 - 4 * a * c

                    # n-avem treaba
                    if delta < 0:
                        pass

                    # se intersecteaza intr-un punct tangent
                    elif delta == 0:
                        # value of lambda when it intersects the planet's orbit
                        lambda_intersect = -b / 2 * a
                        if does_it_crash(lambda_intersect, distance, escape_distanace, cruising_velocity,
                                         escape_time,
                                         x1, x2, y1, y2, planet):
                            crashes = True
                            # lasa, uita-te in alta zi
                            break

                    # delta > 0, 2 intersectii
                    else:
                        # the two lambda points of intersection
                        lamb1 = (-b + sqrt(delta)) / 2 * a
                        lamb2 = (-b - sqrt(delta)) / 2 * a

                        for lambda_intersect in [lamb1, lamb2]:
                            if does_it_crash(lambda_intersect, distance, escape_distanace, cruising_velocity,
                                             escape_time, x1, x2, y1, y2, planet):
                                crashes = True
                                break
                        if crashes:
                            # lasa, uita-te in alta zi nu te mai uita la alte plenete
                            break

            if not crashes:
                min_distance = distance
                optimal_transfer_window_day = day
                optimal_cruising_time = cruising_time

    if optimal_transfer_window_day == -1:
        return False

    # amu plecam la drum
    travel_results = {}

    travel_results['escape_time'] = escape_time
    travel_results['escape_distance'] = escape_distanace
    travel_results['optimal_transfer_window_day'] = optimal_transfer_window_day

    travel_results['cruise_time'] = optimal_cruising_time

    travel_results['total_travel_time'] = travel_results['cruise_time'] + 2 * escape_time

    travel_results["start_angular_positions"] = get_angular_positions(planets, t0 + optimal_transfer_window_day)
    travel_results["end_angular_positions"] = get_angular_positions(planets,
                                                                    t0 + optimal_transfer_window_day + travel_results[
                                                                        'total_travel_time'])

    return travel_results


def does_it_crash(lambda_intersect, distance, escape_distance, cruising_velocity, escape_time, x1, x2, y1, y2,
                  planet: dict):
    # value of lambda at escape distance
    lambda_escape = (distance - escape_distance) / distance

    # the distance trevevlled from the escape distance to the intersection with the orbit
    d_cruise_intersect = distance * (1 - lambda_intersect) - distance * (1 - lambda_escape)
    # the took to travel the above distance
    t_cruise_intersect = d_cruise_intersect / cruising_velocity
    # the time from take-off to intersection in seconds
    t_intersect = escape_time + t_cruise_intersect
    # make it in days just because
    t_intersect = t_intersect / 86400
    angular_speed = 360 / planet['period']
    # the degrees by which the planet will have moved in that time
    angular_movement = t_intersect * angular_speed
    # the new angular position of the planet when the rocket intersects its orbit
    new_angle = (+ angular_movement) % 360

    # position of that planet at that time
    x_planet = planet['orbital_radius'] * AU * cos(new_angle)
    y_planet = planet['orbital_radius'] * AU * sin(new_angle)

    # position of our rocket at that time
    [xintersect, yintersect] = [lambda_intersect * x1 + (1 - lambda_intersect) * x2,
                                lambda_intersect * y1 + (1 - lambda_intersect) * y2]

    if sqrt((xintersect - x_planet) ** 2 + (yintersect - y_planet) ** 2) <= (planet['diameter'] * (10 ** 3) / 2) ** 2:
        return True


def get_angular_position(period, day: float) -> float:
    """
    :param period: Number of days it takes for a rotation around orbit
    :param day: day in which we are making the measurment
    :return: the angle in degrees
    """
    angular_speed = 360 / period  # degrees per day
    return (day * angular_speed) % 360


def get_angular_positions(planets, day: int) -> [dict[int, float, int]]:
    """
    :param planets: list of planets with orbital radii and periods
    :param day: the day for which we want the positions
    :return: dict of tuples key : planet_name : (angular_position, orbit_radius, planet_radius)
    """

    angular_positions = {}
    for planet in planets:
        angular_speed = 360 / planet['period']  # degrees per day
        angular_position = (day * angular_speed) % 360  # degrees but it wraps around if it goes over 360
        orbit_radius = planet['orbital_radius'] * AU
        planet_radius = planet['diameter'] / 2
        angular_positions[planet['name']] = [angular_position, orbit_radius, planet_radius]

    return angular_positions


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


def calculate_cruise_time(distance, escape_distance, radius_from_planet, radius_to_planet,
                          cruising_velocity) -> float:
    return (
            distance - 2 * escape_distance - radius_from_planet - radius_to_planet) / cruising_velocity


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
