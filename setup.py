
import io
from distutils.core import setup

# deciding to use cython or not based on its successful import
USE_CYTHON : bool = True
try:
    from Cython.Build import cythonize
except ModuleNotFoundError:
    print('unable to retrieve cython, will resort to pure python installation')
    USE_CYTHON = False

# load the version from version.py
version = {}
with open("similaritymeasures/version.py") as fp:
    exec(fp.read(), version)

# based on the option of using cython or not the ext_modules variable is set
if USE_CYTHON:
    ext_modules = cythonize('similaritymeasures/similaritymeasures.py', language='c++')
else:
    ext_modules = []

setup(
    name='similaritymeasures',
    version=version["__version__"],
    author='Charles Jekel',
    author_email='cjekel@gmail.com',
    packages=['similaritymeasures'],
    ext_modules=ext_modules,
    url='https://github.com/cjekel/similarity_measures',
    license='MIT License',
    description='Quantify the difference between two arbitrary curves in space',  # noqa E501
    long_description=io.open('README.rst', encoding="utf-8").read(),
    # long_description_content_type='text/markdown',
    platforms=['any'],
    install_requires=[
        "numpy >= 1.14.0",
        "scipy >= 0.19.0",
        "cython >= 3.0.3"
    ],
)
