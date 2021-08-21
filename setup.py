from setuptools import setup, find_packages
exec(open("journalMiner/__init__.py").read())  # loads __version__


DESCRIPTION = 'Python CLI for mining scientific literature.'
LONG_DESCRIPTION = 'This package contains a CLI that allows mining of the EUPMC database for papers that contain hits for keywords.'

# Setting up
setup(
        name="journal-miner",
        version= __version__,
        author="George Pearse, James Sanders",
        author_email="james.sanders1711@gmail.com",
        url = 'https://github.com/J-E-J-S/pyminer',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'beautifulsoup4==4.9.3',
            'pandas==1.2.2',
            'click==7.1.2'
        ],
        entry_points = {
            'console_scripts':['pyminer=journalMiner.pyminer:cli']
        }
)
