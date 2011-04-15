from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='solder',
    version=version,
    description="Incredibly light-weight template-less web development.",
    long_description="""
    WTF?  Another one? I think this one's different. You'll see why...
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Marlin Forbes',
    author_email='marlinf@datashaman.com',
    url='https://github.com/datashaman/solder',
    license='Open Source Initiative OSI - The MIT License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    dependency_links=[
        './dist',
    ],
    install_requires=[
        'pastescript',
        'pyquery',
        'lxml',
        'routes',
        'simplejson',
        'webob',
        'beaker',
        'yolk',
        'beaker_extensions',
        'webhelpers',
        'decorator',
        'redis',
        'redisco',
        'repoze.what-quickstart',
        'faker',
        'weberror',
    ],
    tests_require=[
        'faker',
    ],

    # install_requires=[
        # -*- Extra requirements: -*-
        # 'welder',
        # 'yolk',
        # 'pastedeploy',
        # 'setuptools-git',
        # 'repoze.what-quickstart',
        # 'redis',
        # 'redisco',
        # 'pyquery',
        # 'python-faker',
        # 'routes',
        # 'funkload',
        # 'beaker',
        # 'beaker_extensions',
        # 'webhelpers',
        # 'decorator',
        # 'simplejson',
        # 'repoze.profile',
        # 'pipe',
    # ],

    entry_points={
      'paste.app_factory': [
          'main = solder:make_app'
      ],
      'paste.app_install': [
          'main = pylons.util:PylonsInstaller'
      ],
      'paste.filter_factory': [
          'repoze = repoze.what.plugins.quickstart:add_auth_from_config'
      ],
    }
)
