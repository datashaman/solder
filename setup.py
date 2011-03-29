from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='myapp',
    version=version,
    description="",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    dependency_links=[
        'vendor'
    ],
    install_requires=[
        # -*- Extra requirements: -*-
        'yolk',
        'pastescript',
        'pastedeploy',
        'setuptools-git',
        'repoze.what-quickstart',
        'redis',
        'redisco',
        'pyquery',
        'python-faker',
    ],
    entry_points={
      'paste.app_factory': [
          'main = myapp:make_app'
      ],
      'paste.app_install': [
          'main = pylons.util:PylonsInstaller'
      ],
      'paste.filter_factory': [
          'repoze = repoze.what.plugins.quickstart:add_auth_from_config'
      ],
    }
    )
