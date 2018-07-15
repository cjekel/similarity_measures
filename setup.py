from distutils.core import setup
setup(
    name='similaritymeasures',
    version=open('similaritymeasures/VERSION').read().strip(),
    author='Charles Jekel',
    author_email='cjekel@gmail.com',
    packages=['similaritymeasures'],
    package_data={'similaritymeasures': ['VERSION']},
    url='https://github.com/cjekel/Similarity_measures_for_identifying_material_parameters_from_hysteresis_loops_using_inverse_analysis',
    license='MIT License',
    description='Quantify the difference between two arbitrary curves in 2D space',
    long_description=open('README.rst').read(),
    platforms=['any'],
    install_requires=[
        "numpy >= 1.14.0",
        "scipy >= 0.19.0",
    ],
)
