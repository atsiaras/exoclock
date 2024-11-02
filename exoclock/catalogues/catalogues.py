
__all__ = ['get_planet', 'get_system', 'get_all_planets', 'locate_planet', 'locate_system', 'get_all_planets']

import numpy as np


from .simbad import simbad_search_by_name

from ..spacetime.angles import *
from ..spacetime.angles import _request_angle, _reformat_or_request_angle
from ..spacetime.targets import *
from ..databases import exoclock_data
from ..errors import *


def _flat_name(name):

    flat_name_list = [
        [' ', ''],
        ['-', ''],
        ['cancri', 'cnc'],
        ['hatp10', 'wasp11'],
        ['wasp40', 'hatp27'],
        ['wasp51', 'hatp30'],
        ['wasp86', 'kelt12'],
        ['kelt22', 'wasp173'],
    ]

    name = name.lower()

    for char in flat_name_list:
        name = name.replace(char[0], char[1])

    return name


def _search_by_planet(name):

    planets = exoclock_data.ecc()['planets']

    name_or = name

    if name in planets:
        return name

    else:
        for i in planets:
            if _flat_name(i) == _flat_name(name):
                return str(i)
            elif (_flat_name(i)[-1] == _flat_name(name)[-1] and _flat_name(i)[:-2] == _flat_name(name)[:-1] and
                  _flat_name(i)[-2] in ['a', 'b', 'n']):
                return str(i)

    raise ExoClockInputError('No planet {0} found in the catalogue.'.format(name_or))


def get_all_planets():

    return list(exoclock_data.ecc()['planets'].keys())


def get_planet(name):

    name = _search_by_planet(name)

    planet_data = exoclock_data.ecc()['planets'][name]
    star_data = exoclock_data.ecc()['stars'][planet_data['star']]
    star_data['ra_deg'] = Hours(star_data['ra']).deg()
    star_data['dec_deg'] = Degrees(star_data['dec']).deg_coord()

    return {'name': name, 'planet': planet_data, 'star': star_data}


def get_system(star_name):

    target = simbad_search_by_name(star_name)
    if not target:
        return []

    test = list(set(target.all_names).intersection(list(exoclock_data.ecc()['hosts'])))

    if len(test) == 0:
        return []

    planets = exoclock_data.ecc()['hosts'][test[0]]

    return [get_planet(planet) for planet in planets]


def locate_planet(ra, dec, radius=Degrees(0.02), observation_time=None, observation_type=None):

    _request_angle(ra)
    _request_angle(dec)
    _request_angle(radius)

    pointing = FixedTarget(ra, dec)

    test_planets = []

    for test_planet_name in get_all_planets():
        test_planet = get_planet(test_planet_name)
        test_planet = FixedTarget(Degrees(test_planet['star']['ra_deg']), Degrees(test_planet['star']['dec_deg']))
        test_planets.append([pointing.distance_on_sphere(test_planet).deg(), test_planet_name])

    test_planets.sort()

    if test_planets[0][0] < radius.deg():
        return get_planet(test_planets[0][1])
    else:
        raise ExoClockLibraryError('Planet could not be located')


def locate_system(ra, dec, radius=0.02):

    return get_system(locate_planet(ra, dec, radius)['star']['simbad_id'])


def get_all_planets():
    return list(exoclock_data.ecc()['planets'].keys())


