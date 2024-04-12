from setuptools import setup, find_packages


setup(
    name='pftl',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        "console_scripts": ["py4lab = pftl.start:start"]
        },
    )