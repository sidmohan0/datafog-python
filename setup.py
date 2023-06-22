#  package using pip, navigate to the directory that contains the setup.py file and type pip install .
from setuptools import setup, find_packages



# Read README for the long description
with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='datafog',
    version='1.3.7',  # versioning of your package
    packages=find_packages(),  # automatically find all packages
    author='Sid Mohan',
    author_email='sid@datafog.dev',
    description='A Python package for data anonymization',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    install_requires=['faker', 'pandas', 'sqlalchemy'],
    classifiers=[
        'License :: OSI Approved :: BSD License',  # Choose a license
        'Programming Language :: Python :: 3.10',  # Python version
        # etc.
    ],
)
