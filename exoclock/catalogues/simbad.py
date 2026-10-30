__all__ = ['simbad_search_by_name', 'simbad_search_by_coordinates', 'reconnect_to_simbad', 'get_simbad_status']

import time
import urllib
import requests
import warnings

from astroquery.simbad import Simbad

from ..spacetime.angles import *
from ..spacetime.moments import now
from ..spacetime.angles import _request_angle, _reformat_or_request_angle
from ..spacetime.targets import *
from ..databases import exoclock_data
from ..errors import *

Simbad = Simbad()
Simbad.add_votable_fields('ids')

Simbad.SIMBAD_URL = None
Simbad.TIMEOUT = 5

# check simbad url
def check_simbad_server(force_fail=False):

    if not Simbad.SIMBAD_URL:

        print('exoclock: Checking Simbad server...')

        for url in [
            'https://simbad.cds.unistra.fr/simbad',
            'https://simbad.idia.ac.za/simbad',
            'https://simbad.cfa.harvard.edu/simbad'
        ]:
            try:
                if force_fail:
                    print(error)
                _ = urllib.request.urlopen(url, timeout=5)
                Simbad.SIMBAD_URL = url + '/sim-script'
                print('connected to: ', url)
                return True
            except:
                print('failed to connect to: ', url)
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
        message = 'Connected to ' + Simbad.SIMBAD_URL

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


def _fix_simbad_coordinates(input):

    input = str(input).replace(' ', ':')

    if len(input.split(':')) == 1:
        input += ':00:00'
    elif len(input.split(':')) == 2:
        input += ':00'

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
        except requests.ConnectionError:
            print('Simbad disconnected.')
            Simbad.SIMBAD_URL = 'unavailable'

        if result and len(result) > 0:

            return FixedTarget(
                Hours(_fix_simbad_coordinates(result[0]['RA'])),
                Degrees(_fix_simbad_coordinates(result[0]['DEC'])),
                _fix_simbad_name(result[0]['MAIN_ID']),
                [_fix_simbad_name(ff) for ff in result[0]['IDS'].split('|')]
            )

        else:
            print(star_name + ': No matches found.')
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
                result = Simbad.query_region("{0}d {1}d".format(target.ra.deg(), target.dec.deg()),
                                             radius='{0}d'.format(radius.deg()))
        except requests.ConnectionError:
            print('Simbad disconnected.')
            Simbad.SIMBAD_URL = 'unavailable'

        if result and len(result) > 0:
            return FixedTarget(
                Hours(_fix_simbad_coordinates(result[0]['RA'])),
                Degrees(_fix_simbad_coordinates(result[0]['DEC'])),
                _fix_simbad_name(result[0]['MAIN_ID']),
                [_fix_simbad_name(ff) for ff in result[0]['IDS'].split('|')]
            )
        else:
            print('No matches found.')
            return None

    else:
        print('Simbad disconnected.')
        return None
