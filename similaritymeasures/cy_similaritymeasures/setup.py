'''
knowing this may be a bad thing, but i will place here a
quick setup.py to just
'''

from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name = "cy_frechet",
    ext_modules = cythonize(Extension(
        "cy_similaritymeasures",
        sources=["cy_similaritymeasures.pyx"],
        language="c++"
    )
))

