"""
django_trace
-----------
django_trace is a python package for monitoring your django web app
`````
* Source
  https://github.com/kouroshparsa/django_trace
"""
from setuptools import Command, setup, find_packages
import os
from distutils import sysconfig;
inc_path = sysconfig.get_config_vars()['INCLUDEPY']

version = '1.10'
import sys
setup(
    name='django_trace',
    version=version,
    url='https://github.com/kouroshparsa/django_trace',
    download_url='https://github.com/kouroshparsa/django_trace/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='A package for monitoring your django web app',
    long_description=__doc__,
    packages=find_packages(),
    install_requires = ['django>=1.8'],
    python_requires='>=2.7',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python'
    ]
)
