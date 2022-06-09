import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pylevis',
    version='0.215',
    description='Python utilities/interface for VENUS-LEVIS fast particle orbit code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=['Programming Language :: Python :: 3',
                'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                'Topic :: Scientific/Engineering'],
    url='https://github.com/Spiffmeister/pyLEVIS',
    author='Dean Muir',
    license='GNU 3.0',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy','matplotlib'],
    include_package_data=True
)