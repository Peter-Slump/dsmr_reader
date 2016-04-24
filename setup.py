from setuptools import setup, find_packages

setup(
    name='DSMR Reader',
    packages=find_packages(),
    install_requires=[
        'pyserial==3.0.1',
        'pytz==2016.3'
    ]
)

