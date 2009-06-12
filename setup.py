#!/usr/bin/env python

from distutils.core import setup

setup(
    name='d51_django_db',
    version='0.1',
    description='Django model manager for using specific database configurations with a model',
    author='Travis Swicegood',
    author_email='development@domain51.com',
    url='http://github.com/tswicegood/d51_django_db',
    package_dir={
        'd51_django_db': 'src',
    },
    packages=[
        'd51_django_db', 
    ],
    license="CDDL http://opensource.org/licenses/cddl1.php",
)

