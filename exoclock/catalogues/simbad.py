__all__ = ['simbad_search_by_name', 'simbad_search_by_coordinates', 'reconnect_to_simbad', 'get_simbad_status']

import time
import urllib
import requests
import warnings
import astropy.units as units
import astroquery.simbad

from astropy.coordinates import SkyCoord

from ..spacetime.angles import *
from ..spacetime.moments import now
from ..spacetime.angles import _request_angle, _reformat_or_request_angle
from ..spacetime.targets import *
from ..databases import exoclock_data
from ..errors import *


astroquery.simbad.conf.servers_list.append('simbad.idia.ac.za')

Simbad = astroquery.simbad.Simbad()

Simbad.SIMBAD_URL = None

# check simbad url
def check_simbad_server(force_fail=False):

    if not Simbad.SIMBAD_URL:

        print('exoclock: Checking Simbad server...')

        for server in [
            'simbad.cds.unistra.fr',
            'simbad.idia.ac.za',
            'simbad.cfa.harvard.edu'
        ]:
            url = 'https://' + server + '/simbad'
            try:
                if force_fail:
                    print(error)
                _ = urllib.request.urlopen(url, timeout=5)
                Simbad.server = server
                Simbad.SIMBAD_URL = url + '/sim-script'
                Simbad.timeout = 5
                print('connected to: ', server)
                return True
            except:
                print('failed to connect to: ', server)
                pass

        if not Simbad.SIMBAD_URL:
            Simbad.SIMBAD_URL = 'unavailable'
            return False

    elif Simbad.SIMBAD_URL == 'unavailable':
        return False

    else:
        return True

check_simbad_server()

def get_simbad_status():

    if Simbad.SIMBAD_URL == 'unavailable':
        message = 'Disconnected'

    else:
        message = 'Connected to ' + Simbad.server

    message += '\n({0} UTC)'.format(now().utc().isoformat())

    return message


def reconnect_to_simbad(force_fail=False):

    Simbad.SIMBAD_URL = None

    _ = check_simbad_server(force_fail=force_fail)


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


def _fix_simbad_name(input):

    try:
        input = input.decode("utf-8")
    except:
        pass

    while '  ' in input:
        input = input.replace('  ', ' ')

    return input

def simbad_search_by_name(star_name, reconnect=False):

    try:
        star = exoclock_data.ecc()['stars'][exoclock_data.ecc()['flats'][_flat_name(star_name)]]

        return FixedTarget(
            Hours(star['ra']),
            Degrees(star['dec']),
            star['simbad_id'],
            [star['simbad_id']]
        )

    except KeyError:
        pass

    if reconnect:
        reconnect_to_simbad()

    if check_simbad_server():

        star_name = star_name.replace('HD-', 'HD ')
        star_name = star_name.replace('HR-', 'HR ')
        star_name = star_name.replace('2MASS-', '2MASS ')
        star_name = star_name.replace('GJ-', 'GJ ')
        star_name = star_name.replace('HIP-', 'HIP ')
        star_name = star_name.replace('LHS-', 'LHS ')
        star_name = star_name.replace('TYC-', 'TYC ')
        star_name = star_name.replace('KIC-', 'KIC ')
        star_name = star_name.replace('ADS-', 'ADS ')
        star_name = star_name.replace('GSC-', 'GSC ')
        star_name = star_name.replace('UCAC4-', 'UCAC4 ')

        if 'BD' in star_name:
            star_name = star_name[:3] + star_name[3:].replace('-', ' ')

        result = None
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                result = Simbad.query_object(star_name)

            if result and len(result) > 0:

                return FixedTarget(
                    Degrees(result[0]['ra']), Degrees(result[0]['dec']),
                    _fix_simbad_name(result[0]['main_id']),
                    list(Simbad.query_objectids(result[0]['main_id'])['id'])
                )

            else:
                print(star_name + ': No matches found.')
                return None

        except requests.ConnectionError:
            print('Simbad disconnected.')
            Simbad.SIMBAD_URL = 'unavailable'
            return None

    else:
        print('Simbad disconnected.')
        return None


def simbad_search_by_coordinates(ra, dec, radius=Degrees(0.02), reconnect=False):

    if reconnect:
        reconnect_to_simbad()

    if check_simbad_server():

        _request_angle(ra)
        _request_angle(dec)
        _request_angle(radius)

        target = FixedTarget(ra, dec)

        result = None
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                result = Simbad.query_region(
                    SkyCoord(
                        target.ra.deg(), target.dec.deg(), unit=(units.deg, units.deg), frame='icrs'),
                    radius=radius.deg() * units.deg
                )

            if result and len(result) > 0:

                list_to_sort = [[
                    target.distance_on_sphere(
                        FixedTarget(Degrees(result[row]['ra']), Degrees(result[row]['dec']))
                    ).deg(), row ] for row in range(len(result)) ]

                list_to_sort.sort()

                row = list_to_sort[0][1]

                return FixedTarget(
                    Degrees(result[row]['ra']), Degrees(result[row]['dec']),
                    _fix_simbad_name(result[row]['main_id']),
                    list(Simbad.query_objectids(result[row]['main_id'])['id'])
                )
            else:
                print('No matches found.')
                return None

        except requests.ConnectionError:
            print('Simbad disconnected.')
            Simbad.SIMBAD_URL = 'unavailable'
            return None

    else:
        print('Simbad disconnected.')
        return None
