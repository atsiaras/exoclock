
import datetime
import pytest
import exoclock
import numpy as np

from astropy.time import Time
from exoclock.spacetime.moments import _request_time


def test_times():

    astropy_test_era = Time('2022-01-01T12:00:00.0').earth_rotation_angle(0).arcsec
    dtime = datetime.timedelta(hours=1)
    ref = exoclock.Moment('2022-01-01T11:30:00.0')
    now = exoclock.now()

    for test_time in [
        exoclock.Moment(datetime.datetime(2022, 1, 1, 12, 0, 0, microsecond=0)),
        exoclock.Moment('2022-01-01T12:00:00.0'),
        exoclock.Moment('2022-01-01T12:00:00.0000001'),
        exoclock.Moment('2022-01-01T12:00:00.0Z'),
        exoclock.Moment('2022-01-01T12:00:00.0+00'),
        exoclock.Moment('2022-01-01T12:00:00.0+00:00'),
        exoclock.Moment('2022-01-01T12:30:00.0+0030'),
        exoclock.Moment('2022-01-01T11:30:00.0-0030'),
        exoclock.Moment(jd_utc=2459581.0),
    ]:

        assert test_time.leap_seconds() == 37
        assert round(test_time.ut1_utc_diff(), 6) == -0.110460

        assert (test_time + dtime).utc() == datetime.datetime(2022, 1, 1, 13, 0, 0)
        assert (test_time - dtime).utc() == datetime.datetime(2022, 1, 1, 11, 0, 0)
        assert test_time - ref == datetime.timedelta(hours=0.5)

        assert test_time.utc() == datetime.datetime(2022, 1, 1, 12, 0, 0)
        assert test_time.tai() == datetime.datetime(2022, 1, 1, 12, 0, 37)
        assert test_time.tt() == datetime.datetime(2022, 1, 1, 12, 1, 9, 184000)
        assert test_time.ut1() == datetime.datetime(2022, 1, 1, 11, 59, 59, 889540)

        assert round(test_time.jd_utc(), 6) == 2459581.0
        assert round(test_time.jd_tai(), 6) == 2459581.000428
        assert round(test_time.jd_tt(), 6) == 2459581.000801
        assert round(test_time.jd_ut1(), 6) == 2459580.999999

        assert round(test_time.era()._arcseconds, 3) == round(astropy_test_era, 3)

        print(test_time.__repr__)
        _request_time(test_time)

    for utc in [
        10,
        'a',
        '2022-01-01T12:00:00.0+00100',
        '2022-01-01T1:00:00.0',
        '2022-01-01T1.1:00:00.0',
        '2022-01-01T1a:00:00.0',
        '1960-01-01T12:00:00',
    ]:
        with pytest.raises(exoclock.ExoClockInputError):
            exoclock.Moment(utc)

    for utc in [
        '2022-01-01T121:00:00.0',
    ]:
        with pytest.raises(ValueError):
            exoclock.Moment(utc)

    for jd_utc in [
            10,
            'a',
        ]:
            with pytest.raises(exoclock.ExoClockInputError):
                exoclock.Moment(jd_utc=jd_utc)

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Moment('2022-01-01T12:00:00.0', 2459581.0)

    with pytest.raises(exoclock.ExoClockInputError):
        _request_time('a')

    with pytest.raises(exoclock.ExoClockInputError):
        _ = test_time + 10

    with pytest.raises(exoclock.ExoClockInputError):
        _ = test_time - 10


def test_utc_bjd():

    ra = 48.75
    dec = 45.7

    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 2458485.0, 'JD_UTC'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 58484.5, 'MJD_UTC'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 2458485.0046340, 'BJD_TDB'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 2458485.0038333, 'BJD_UTC'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 2458485.0046033, 'HJD_TDB'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, 2458485.00380255, 'HJD_UTC'), 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([2458485.00000000]), 'JD_UTC')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([0058484.50000000]), 'MJD_UTC')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([2458485.00463400]), 'BJD_TDB')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([2458485.00383330]), 'BJD_UTC')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([2458485.00460330]), 'HJD_TDB')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_bjd_tdb(ra, dec, np.array([2458485.00380255]), 'HJD_UTC')[0], 7) == 2458485.0046340
    assert round(exoclock.convert_to_jd_utc(ra, dec, 2458485.0, 'JD_UTC'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, 58484.5, 'MJD_UTC'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, 2458485.0046340, 'BJD_TDB'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, 2458485.0038333, 'BJD_UTC'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, 2458485.0046033, 'HJD_TDB'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, 2458485.00380255, 'HJD_UTC'), 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([2458485.00000000]), 'JD_UTC')[0], 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([0058484.50000000]), 'MJD_UTC')[0], 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([2458485.00463400]), 'BJD_TDB')[0], 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([2458485.00383330]), 'BJD_UTC')[0], 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([2458485.00460330]), 'HJD_TDB')[0], 7) == 2458485.0
    assert round(exoclock.convert_to_jd_utc(ra, dec, np.array([2458485.00380255]), 'HJD_UTC')[0], 7) == 2458485.0

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_bjd_tdb(ra, dec, 2458485.0, 'aaa')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_bjd_tdb(ra, dec, [2458485.0], 'aaa')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_bjd_tdb(ra, dec, 'a', 'JD_UTC')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_bjd_tdb(ra, dec, np.array(['a']), 'JD_UTC')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_jd_utc(ra, dec, 2458485.0, 'aaa')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_jd_utc(ra, dec, [2458485.0], 'aaa')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_jd_utc(ra, dec, 'a', 'JD_UTC')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.convert_to_jd_utc(ra, dec, np.array(['a']), 'JD_UTC')


