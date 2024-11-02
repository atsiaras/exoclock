
import pytest
import exoclock
from exoclock.catalogues.simbad import _fix_simbad_coordinates


def test_ecc():

    planet1 = exoclock.get_planet('hatp7b')
    planet2 = exoclock.get_planet('HAT-P-7b')
    assert planet1['name'] == 'HAT-P-7b'
    assert planet2['name'] == 'HAT-P-7b'
    assert planet1['planet']['sma_over_rs'] == planet2['planet']['sma_over_rs']

    planet = exoclock.get_planet('wasp77b')
    assert planet['name'] == 'WASP-77Ab'

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.get_planet('aaaaaaaaaa')

    assert len(exoclock.get_all_planets()) > 0

    planet = exoclock.locate_planet(exoclock.Degrees(330.795), exoclock.Degrees(18.884))
    assert planet['name'] == 'HD209458b'

    planet = exoclock.locate_planet(exoclock.Degrees(330.795), exoclock.Degrees(18.884), exoclock.Degrees(0.1))
    assert planet['name'] == 'HD209458b'

    with pytest.raises(exoclock.ExoClockLibraryError):
        exoclock.locate_planet(exoclock.Degrees(330.795), exoclock.Degrees(17.884))

    assert exoclock.get_system('HD189987976') == []
    assert exoclock.get_system('M42') == []
    assert len(exoclock.get_system('HD209458b')) == 1

    assert len(exoclock.locate_system(exoclock.Degrees(330.795), exoclock.Degrees(18.884), exoclock.Degrees(0.1))) == 1


def test_simbad():

    target = exoclock.simbad_search_by_name('TYC 1949-1705-1')

    assert target.name == 'TYC 1949-1705-1'

    target = exoclock.simbad_search_by_name('XO-1')

    assert target.name == 'BD+28 2507'

    target = exoclock.simbad_search_by_coordinates(target.ra, target.dec)

    assert target.name == 'BD+28 2507b'

    assert _fix_simbad_coordinates('16') == '16:00:00'
    assert _fix_simbad_coordinates('16:00') == '16:00:00'

    assert exoclock.simbad_search_by_name('BDXXXXXXXXXXXXXXXXX') is None
    assert exoclock.simbad_search_by_coordinates(exoclock.Hours(1), exoclock.Degrees(0), radius=exoclock.Degrees(0.001)) is None
