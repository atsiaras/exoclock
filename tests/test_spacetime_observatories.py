
import datetime
import numpy as np
import pytest
import exoclock

from exoclock.spacetime.observatories import _request_observatory, _Horizon


def test_observing():

    with pytest.raises(exoclock.ExoClockInputError):
        _Horizon('xxx').horizon(exoclock.Degrees(10)).deg()

    with pytest.raises(exoclock.ExoClockInputError):
        _Horizon({}).horizon(exoclock.Degrees(10)).deg()

    assert _Horizon(20).horizon(exoclock.Degrees(10)).deg() == 20
    assert _Horizon('0 20\n90 20\n180 20\n270 20\n').horizon(exoclock.Degrees(10)).deg() == 20
    assert _Horizon([[0, 20], [90, 20], [180, 20], [270, 20]]).horizon(exoclock.Degrees(10)).deg() == 20
    assert _Horizon(np.array([[0, 20], [90, 20], [180, 20], [270, 20]])).horizon(exoclock.Degrees(10)).deg() == 20

    with pytest.raises(exoclock.ExoClockInputError):
            exoclock.Observatory(exoclock.Degrees(140), exoclock.Degrees(23), 2)

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Observatory(exoclock.Degrees(40), exoclock.Degrees(23), 'x')

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Observatory(exoclock.Degrees(40), exoclock.Degrees(23), 20)

    with pytest.raises(exoclock.ExoClockError):
        _request_observatory('a')

    observatory = exoclock.Observatory(exoclock.Degrees(40), exoclock.Degrees(-23), -2)
    print(observatory.__repr__)
    _request_observatory(observatory)
    assert observatory.coord() == '+40:00:00.0 337:00:00.0'
    assert observatory.lt(exoclock.Moment(jd_utc=2459903)) == datetime.datetime(2022, 11, 19, 10, 0, 0)
    assert round(observatory.lera(exoclock.Moment(jd_utc=2459903)).deg(), 1) == 215.20

    observatory = exoclock.Observatory(exoclock.Degrees(40), exoclock.Degrees(23), 2)
    print(observatory.__repr__)
    _request_observatory(observatory)
    assert observatory.coord() == '+40:00:00.0 23:00:00.0'
    assert observatory.lt(exoclock.Moment(jd_utc=2459903)) == datetime.datetime(2022, 11, 19, 14, 0, 0)
    assert round(observatory.lera(exoclock.Moment(jd_utc=2459903)).deg(), 1) == 261.20

    moment = exoclock.Moment(jd_utc=2459903)
    target = exoclock.simbad_search_by_name('XO-1')
    assert round(observatory.target_azimuth_altitude(target,  moment)[0].deg()) == 62.0
    assert round(observatory.airmass(target,  moment), 1) == 1.1
    assert observatory.is_target_visible(target,  moment)
    assert len(observatory.target_horizon_crossings(target, moment, 1)) == 2
    assert len(observatory.target_altitude_crossings(target, moment, 1, exoclock.Degrees(20))) == 2

    moment = exoclock.Moment(jd_utc=2459903)
    target = exoclock.simbad_search_by_name('HD189733')
    assert round(observatory.target_azimuth_altitude(target,  moment)[0].deg()) == 286.0
    assert round(observatory.airmass(target,  moment), 1) == 1.3
    assert observatory.is_target_visible(target,  moment)
    assert len(observatory.target_horizon_crossings(target, moment, 1)) == 2
    assert len(observatory.target_altitude_crossings(target, moment, 1, exoclock.Degrees(20))) == 2

    moment = exoclock.Moment('2022-05-01T12:00:00')
    target = exoclock.simbad_search_by_name('XO-1')
    assert len(observatory.periodic_events_visibility(target, moment, 1, 2455787.553228, 'BJD_TDB', 3.94150468, 5/24)) == 1

