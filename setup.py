
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='evolven',
    version='1.1.0',

    description='Evolven API Python Client',
    long_description_content_type='text/markdown',
    long_description=long_description,

    url='https://github.com/evolven-software/evolven-api-python',

    author='Evolven Data Science Team',
    author_email='bostjan@evolven.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Information Analysis',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='evolven api development',

    packages=find_packages(exclude=['examples']),
)