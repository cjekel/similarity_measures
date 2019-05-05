from .similaritymeasures import *  # noqa F403
import os  # noqa F401

# add rudimentary version tracking
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(VERSION_FILE).read().strip()
