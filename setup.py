import setuptools

setuptools.setup(
    name='pylevis',
    version='0.2',
    description='Python utilities/interface for VENUS-LEVIS fast particle orbit code',
    classifiers=['Programming Language :: Python :: 3',
                'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                'Topic :: Scientific'],
    url='https://github.com/Spiffmeister/pyLEVIS',
    author='Dean Muir',
    license='GNU 3.0',
    packages=setuptools.find_packages('pylevis'),
    package_dir={'':'pylevis'},
    python_requires='>=3.6',
)