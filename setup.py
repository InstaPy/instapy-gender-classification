from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Tim Grossmann'

requirements = [
    'selenium',
    'requests'
]

description = 'Training data generation for InstaPy gender classification'

setup(
    name='instapy_gender_class',
    version=__version__,
    author=__author__,
    author_email='contact.timgrossmann@gmail.com',
    url='https://github.com/timgrossmann/InstaPy',
    py_modules='instapy_class',
    description=description,
    install_requires=requirements
)
