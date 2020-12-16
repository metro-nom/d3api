import os
from setuptools import setup, find_packages

__version__ = '20.12.2'

setup(
    author="Markus Leist",
    author_email='markus.leist@metronom.com',
    name='d3api',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'python-dotenv',
        'passlib',
        'apispec[yaml]',
        'apispec-webframeworks',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    license="BSD license",
    keywords='d3',
    entry_points={
        'console_scripts': [
            'd3api = d3api.manage:cli'
        ]
    }
)
