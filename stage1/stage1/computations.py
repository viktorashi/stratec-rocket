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
#
def get_escape_velocities(data:str)->[dict]:
    planets = parse_planets(data)

    for planet in planets:
        if planet['name'] == 'Earth':
            earth_mass = planet['mass']
            break


def parse_planets(file_data:str)->[dict]:
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
                print('avem un pamantt')
                # kg (cam multe)
                mass = 6 * 10 ** 24  # bit cheap but does the job
                earth_mass = mass
            elif earth_mass != -1:
                earths_masses = mass.split(' ')[1]
                mass = earth_mass * float(earths_masses)
            #the ones before earth came up
            else:
                mass = float(mass.split(' ')[1])

            planets.append({
                "name": planet_name,
                "diameter": diameter,
                "mass": mass
            })

            print(planet_name, diameter, mass)

    for planet in planets:
        planet["mass"] = planet["mass"] * earth_mass
        if planet['name'] == 'Earth':
            break

    return planets
