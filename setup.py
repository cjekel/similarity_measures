from setuptools import setup
setup(
    name='similaritymeasures',
    version=open('similaritymeasures/VERSION').read().strip(),
    author='Charles Jekel',
    author_email='cjekel@gmail.com',
    packages=['similaritymeasures'],
    package_data={'similaritymeasures': ['VERSION']},
    url='https://github.com/cjekel/similarity_measures',
    license='MIT License',
    description='Quantify the difference between two arbitrary curves in space',  # noqa E501
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    platforms=['any'],
    install_requires=[
        "numpy >= 1.14.0",
        "scipy >= 0.19.0",
        "setuptools >= 38.6.0",
    ],
)
