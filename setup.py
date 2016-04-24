from setuptools import setup

setup(
    name='DSMR Reader',
    packages=['dsmr_reader'],
    install_requires=[
        'pyserial==3.0.1',
        'pytz==2016.3'
    ]
)

