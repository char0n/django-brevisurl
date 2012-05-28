django-brevisurl
================

django-brevisurl is django app for shortening urls. Brevis is a latin word, which means
short, so the name brevisurl == shorturl or url shortener. The actual creating of short
url is handled by the shortening backend.


Requirements
------------

- python 2.7+
- django


Installation
------------

Install via pypi or copy this module into your project or into your PYTHONPATH.


**Put brevisurl into INSTALLED_APPS in your projects settings.py file**

::

 INSTALLED_APPS = (
     'localeurl',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.admin',
     'django.contrib.sitemaps',
     'web',
     'debug_toolbar',
     'rosetta',
     'south',
     'brevisurl'
 )



**Run syncdb command to create database tables from brevisurl models**

::

 python manage.py syncdb


Configuration
-------------

**django settings.py constants**

::

 # Setting for default brevis backend
 BREVISURL_BACKEND = 'brevisurl.backends.local.BrevisUrlBackend' # Default is 'brevisurl.backends.local.BrevisUrlBackend'


Examples
--------

**Example 1**

Using programmatic approach

::

 from brevisurl import get_connection

 connection = get_connection()
 short_url_obj = connection.shorten_url('http://www.codescale.net/')
 print short_url_obj.shortened_url


**Example 2**

Using programmatic approach with shortcut

::

 from brevisurl import shorten_url

 shor_url_obj = shorten_url('http://www.codescale.net/')
 print shor_url_obj.shortened_url


**Example 3**

Using brevisurl in templates via filter approach

::

 {% load brevisurl %}
 {% url homepage as homepage_url %}
 {{ homepage_url|shorten_url }}


**Example 4**

Using brevisurl in templates with filtered tag approach.
brevisurl comes with special tag called `absurl` that works
exactly the same as `url` django tag but prepends protocol + domain
in front of resovled url path.

::

 {% load brevisurltags %}
 {% absurl homepage as homepage_url %}
 {{ homepage_url|shorten_url }}


Tests
-----

**Tested on evnironment**

- Xubuntu Linux 12.04 LTS precise 64-bit
- python 2.7.3+
- python unittest
- django 1.4

**Running tests**

To run the test run command: ::

 $ python manage.py test brevisurl



Author
------

| char0n (Vladimír Gorej, CodeScale s.r.o.)
| email: gorej@codescale.net
| web: http://www.codescale.net


References
----------

 - http://github.com/char0n/django-brevisurl
 - http://pypi.python.org/pypi/django-brevisurl/
 - http://www.codescale.net/en/community#django-brevisurl