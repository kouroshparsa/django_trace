"""
django_trace
-----------
django_trace is a python package for monitoring your django web app
`````
* Source
  https://github.com/kouroshparsa/django_trace
"""
from setuptools import setup, find_packages
from distutils import sysconfig;
inc_path = sysconfig.get_config_vars()['INCLUDEPY']

version = '2.0.2'
long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django_trace',
    version=version,
    url='https://github.com/kouroshparsa/django_trace',
    download_url='https://github.com/kouroshparsa/django_trace/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='django_trace is a python package for monitoring your django web app',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = ['django>=1.8', 'django-autocomplete-light>=3.8',],
    python_requires='>=2.7',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python'
    ]
)
