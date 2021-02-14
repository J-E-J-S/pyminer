from setuptools import setup, find_packages
import os

VERSION = '1.0'
DESCRIPTION = 'Python CLI for mining scientific literature.'
LONG_DESCRIPTION = 'This package contains a CLI that allows mining of the EUPMC database for papers that contain hits for keywords.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pyminer",
        version=VERSION,
        author="George Pearse, James Sanders",
        author_email="james.sanders1711@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'beautifulsoup4==4.9.3',
            'pandas==1.2.2',
            'click==7.1.2'
        ],
        entry_points = {
            'console_scripts':['pyminer=pyminer.pyminer:cli']
        }

)
