"""Setup module"""
from setuptools import setup

def readfile(filename):
    """Get readfile"""
    with open(filename, 'r+') as readmefile:
        return readmefile.read()

setup(
    name="fixer",
    version="3.0.3",
    description="",
    long_description=readfile('README.md'),
    author="Renato O.",
    url="",
    py_modules=['fixer', 'history'],
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': [
            'fixer = fixer:handle_options'
        ]
    },
)
