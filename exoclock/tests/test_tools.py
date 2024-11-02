
import os
import exoclock


def test_files():

    __location__ = os.path.abspath(os.path.dirname(__file__))

    xx = exoclock.open_dict(os.path.join(__location__, 'test1.pickle'))

    xx = {'a': 1}
    exoclock.save_dict(xx, os.path.join(__location__, 'test.pickle'))
    xx = exoclock.open_dict(os.path.join(__location__, 'test.pickle'))
    os.remove(os.path.join(__location__, 'test.pickle'))
    yy = exoclock.copy_dict(xx)
    assert id(yy) != id(xx)
    del xx, yy

    assert exoclock.open_dict_online('a') is False

    exoclock.download('https://raw.githubusercontent.com/ucl-exoplanets/pylightcurve/master/README.md',
                      os.path.join(__location__, 'test.txt'))
    os.remove(os.path.join(__location__, 'test.txt'))
