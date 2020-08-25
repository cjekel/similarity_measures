
import io
from distutils.core import setup

# load the version from version.py
version = {}
with open("similaritymeasures/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='similaritymeasures',
    version=version["__version__"],
    author='Charles Jekel',
    author_email='cjekel@gmail.com',
    packages=['similaritymeasures'],
    url='https://github.com/cjekel/similarity_measures',
    license='MIT License',
    description='Quantify the difference between two arbitrary curves in space',  # noqa E501
    long_description=io.open('README.rst', encoding="utf-8").read(),
    # long_description_content_type='text/markdown',
    platforms=['any'],
    install_requires=[
        "numpy >= 1.14.0",
        "scipy >= 0.19.0",
    ],
)
