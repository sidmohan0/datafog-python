#  package using pip, navigate to the directory that contains the setup.py file and type pip install .
from setuptools import setup, find_packages




setup(
    name='datafog',
    version='1.0',  # versioning of your package
    packages=find_packages(),  # automatically find all packages
    author='Sid Mohan',
    author_email='sid@datafog.dev',
    description='A Python package that provides several methods for data handling',  # a brief description of your package
    long_description=open('README.md').read(),  # a long description read from the README.md file
    install_requires=['faker', 'pandas','sqlalchemy','sqlalchemy.orm','werkzeug','typing'],  # a list of other Python packages required by this package
    classifiers=[
        'License :: OSI Approved :: BSD License',  # Choose a license
        'Programming Language :: Python :: 3.10',  # Python version
        # etc.
    ],
)
