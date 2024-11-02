
import numpy as np
import pytest
import exoclock

from exoclock.spacetime.angles import _request_angle, _reformat_or_request_angle


def test_angles():

    for test_angle in [exoclock.Degrees(54.61),
                       exoclock.Degrees('54.61'),
                       exoclock.Degrees(54, 36, 36.0),
                       exoclock.Degrees('54:36:36.0'),
                       exoclock.Hours(54.61 / 15.0),
                       exoclock.Hours(54 / 15.0, 36.0 / 15.0, 36.0 / 15.0),
                       exoclock.Rad(54.61 * np.pi / 180.0),
                       _reformat_or_request_angle(54.61)
                       ]:

        assert round(test_angle._arcseconds, 1) == 196596.0
        assert test_angle.dms() == '54:36:36.0'
        assert test_angle.dms_coord() == '+54:36:36.0'
        assert round(test_angle.deg(), 2) == 54.61
        assert round(test_angle.deg_coord(), 2) == 54.61
        assert test_angle.hms() == '03:38:26.4'
        assert round(test_angle.hours(), 4) == 3.6407
        assert round(test_angle.rad(), 10) == 0.9531243045
        assert round(test_angle.sin(), 10) == 0.8152288870
        assert round(test_angle.cos(), 10) == 0.5791388969
        assert round(test_angle.tan(), 10) == 1.4076569392
        assert round(exoclock.arcsin(test_angle.sin()).deg(), 2) == 54.61
        assert round(exoclock.arccos(test_angle.cos()).deg(), 2) == 54.61
        assert round(exoclock.arctan(test_angle.tan()).deg(), 2) == 54.61
        print(test_angle.__repr__)
        _request_angle(test_angle)

    for test_angle in [exoclock.Degrees(-54.61),
                       exoclock.Degrees('-54.61'),
                       exoclock.Degrees(-54, -36, -36.0),
                       exoclock.Degrees('-54:36:36.0'),
                       exoclock.Hours(-54.61 / 15.0),
                       exoclock.Hours(-54 / 15.0, -36.0 / 15.0, -36.0 / 15.0),
                       exoclock.Rad(-54.61 * np.pi / 180.0)]:

        assert round(test_angle._arcseconds, 1) == 1099404.0
        assert test_angle.dms() == '305:23:24.0'
        assert test_angle.dms_coord() == '-54:36:36.0'
        assert round(test_angle.deg(), 2) == 305.39
        assert round(test_angle.deg_coord(), 2) == -54.61
        assert test_angle.hms() == '20:21:33.6'
        assert round(test_angle.hours(), 4) == 20.3593
        assert round(test_angle.rad(), 10) == 5.3300610027
        assert round(test_angle.sin(), 10) == -0.8152288870
        assert round(test_angle.cos(), 10) == 0.5791388969
        assert round(test_angle.tan(), 10) == -1.4076569392
        print(test_angle.__repr__)
        _request_angle(test_angle)

    a1, a2 = exoclock.Degrees(55.0), exoclock.Degrees(5.0)
    assert (a1 + a2).deg() == 60.0
    assert (a1 - a2).deg() == 50.0
    assert (a1 * 2).deg() == 110.0
    assert (2 * a1).deg() == 110.0
    assert (a1 / 2).deg() == 27.5

    assert exoclock.Degrees(5.0).deg_coord() == 5.0
    assert exoclock.Degrees(5.0).dms_coord() == '+05:00:00.0'
    assert exoclock.Degrees(95.0).deg_coord() == 85.0
    assert exoclock.Degrees(95.0).dms_coord() == '+85:00:00.0'
    assert exoclock.Degrees(185.0).deg_coord() == -5.0
    assert exoclock.Degrees(185.0).dms_coord() == '-05:00:00.0'
    assert exoclock.Degrees(275.0).deg_coord() == -85.0
    assert exoclock.Degrees(275.0).dms_coord() == '-85:00:00.0'
    assert _reformat_or_request_angle(exoclock.Degrees(275.0)).dms_coord() == '-85:00:00.0'

    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Degrees('a')
    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Degrees('35:00:00', 10)
    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Degrees(['a'])
    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Degrees(35, -10)
    with pytest.raises(exoclock.ExoClockInputError):
        exoclock.Rad('a')
    with pytest.raises(exoclock.ExoClockError):
        a1 * a2
    with pytest.raises(exoclock.ExoClockError):
        a1 / a2
    with pytest.raises(exoclock.ExoClockError):
        _request_angle('a')
    with pytest.raises(exoclock.ExoClockError):
        _reformat_or_request_angle('a')
