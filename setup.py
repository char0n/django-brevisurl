# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    """Utility function to read the README file.

    Used for the long_description. It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-brevisurl',
    version='1.0',
    description='django-brevisurl is django app for shortening urls',
    long_description=read('README.rst'),
    author=u'Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#django-brevisurl',
    download_url='http://github.com/char0n/django-brevisurl/tarball/master',
    license='BSD',
    keywords = 'url short shortener',
    packages=find_packages('.'),
    install_requires=['django'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
