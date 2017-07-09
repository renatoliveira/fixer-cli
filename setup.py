from setuptools import setup

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()

setup(
    name="fixer",
    version="1.0.0",
    description="",
    long_description=readfile('README.md'),
    author="Renato O.",
    url="",
    py_modules=['fixer'],
    license=readfile('LICENSE')
    entry_points={
        'console_scripts': [
            'fixer = fixer:handle_options'
        ]
    },
)