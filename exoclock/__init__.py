import os

__version__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '__version__.txt')).read()
__author__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '__author__.txt')).read()
__author_email__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '__author_email__.txt')).read()
__description__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '__description__.txt')).read()
__url__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '__url__.txt')).read()

from .catalogues.catalogues import *
from .catalogues.simbad import *

from .spacetime.angles import *
from .spacetime.moments import *
from .spacetime.observatories import *
from .spacetime.targets import *

from .processes.files import *

from .errors import *
from .databases import *
