
__all__ = ['open_dict', 'save_dict', 'copy_dict',
           'download', 'open_dict_online'
           ]

import os
import ssl
import copy
import pickle
import urllib

from urllib.request import urlretrieve


def open_dict(path):

    class Dummy(object):
        def __init__(self, *argv, **kwargs):
            pass

    _ = Dummy(5)

    class Unpickler(pickle._Unpickler):
        def find_class(self, module, name):
            try:
                return super().find_class(module, name)
            except Exception as e:
                print(e)
                return Dummy

    with open(path, 'rb') as f:
        unpickler = Unpickler(f)
        return unpickler.load()


def save_dict(dictionary, path):
    internal_copy = copy_dict(dictionary)
    pickle.dump(internal_copy, open(path, 'wb'), protocol=2)
    del internal_copy


def copy_dict(dictionary):
    return copy.deepcopy(dictionary)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download(link, destination, filename=None, verbose=True):

    if not filename:
        filename = os.path.split(destination)[1]

    if verbose:
        print('    Downloading {0}...'.format(filename))
        print('           from {0} '.format(link))
    try:
        with urllib.request.urlopen(link, context=ctx) as u, \
                open(destination, 'wb') as f:
            f.write(u.read())
        if verbose:
            print('    Done!')
        return True
    except Exception as e:
        print('ERROR: {0}\n    Could not download {1}', e, filename)
        return False


def open_dict_online(link):

    try:
        return pickle.load(urllib.request.urlopen(link, context=ctx))
    except:
        return False

