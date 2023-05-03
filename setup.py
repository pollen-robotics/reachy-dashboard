"""Setup script."""

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


setup(
    name='reachy_dashboard',
    version='0.1',
    packages=find_packages(exclude=['tests']),

    install_requires=[
        'flask',
        'aioflask',
        'pyserial',
        'asgiref',
        'reachy-sdk',
        'reachy-utils',
        ],

    extra_requires={
        'test': ['pytest'],
    },

    author='Pollen Robotics',
    author_email='contact@pollen-robotics.com',
    url='https://github.com/pollen-robotics/RAP-2021',

    description="Dashboard web interface for Reachy 2021 and 2023.",
)
