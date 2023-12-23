from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='myservice',
    version='0.1',
    packages=[''],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'myservice=myservice:main',
        ],
    },
)
