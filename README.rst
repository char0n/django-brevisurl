django-brevisurl
================

django-brevisurl is django app for shortening urls. Brevis is a latin word, which means
short, so the name brevisurl == shorturl or url shortener. The actual creating of short
url is handled by the shortening backend.


Requirements
------------

- python 3.9
- django 4.2


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

 # This bypasses Django Site framework and settings.SITE_ID; if set, brevisurl don't use Django Site framework
 # but uses this settings insted to generate  absolute urls
 BREVISURL_BACKEND_LOCAL_DOMAIN = 'http://brevisurl.net/' # Default is None

 # Characters that are used to generate tokens for local backend.
 BREVISURL_LOCAL_BACKEND_TOKEN_CHARS = list(string.ascii_letters + string.digits)

 # Settings for maximum length for original url (including GET query parameters)
 BREVISURL_LOCAL_ORIGINAL_URL_MAX_LENGTH = 200

 # Settings for token length.
 BREVISURL_LOCAL_BACKEND_TOKEN_LENGTH = 5

 # Settings for url pattern.
 BREVISURL_LOCAL_BACKEND_URL_PATTERN = r'^(?P<token>[a-zA-Z0-9]{' + str(LOCAL_BACKEND_TOKEN_LENGTH) + r'})$'

 # Protocol for local backend.
 BREVISURL_LOCAL_BACKEND_DOMAIN_PROTOCOL = getattr(settings, 'BREVISURL_LOCAL_BACKEND_DOMAIN_PROTOCOL', 'http')


**Append brevisurl url patterns to your urls.py at the end of module, if you're using local backend**

::

 urlpatterns += patterns('',
     # brevisurl urls
     (r'^', include('brevisurl.urls'))
 )

**To be able to access brevisurl settings add brevisurl.context_processors.brevisurl_data to your context processors**

::

 TEMPLATE_CONTEXT_PROCESSORS = (
     'django.contrib.auth.context_processors.auth',
     'django.core.context_processors.debug',
     'django.core.context_processors.request',
     'django.contrib.messages.context_processors.messages',
     'brevisurl.context_processors.brevisurl_data'
 )

**Configure site framework**

This setting is important for local backend only. At least one Site object
must be created and configured as current via settings.SITE_ID. For development/production
switching I suggest you to use configuration like this. Setting is also important
while using `absurl` templatag. Domain for absolute url is generated from current Site object.

::

 if DEBUG:
     SITE_ID = 2 # pk for Site object containing your development domain e.g. 'localhost:8000'
 else:
     SITE_ID = 1 # pk for Site object containing your production domain e.g. 'www.production.net'



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

 {% load brevisurltags %}
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
- django 1.4.1

**Running tests**

To run the test run command: ::

 $ python manage.py test brevisurl


Development setup
-----------------
::

 $ make bootstrap
 $ python manage.py test brevisurl

Tests
-----

**Tested on evnironment**

- Linux Mint 15 Olivia 64-bit
- python 2.7.4
- python unitest

**Running tests**

To run the tests, execute one of the following command:::

 $ python manage.py test brevisurl

Or:::

 $ make test


Author
------

| char0n (Vladimír Gorej, CodeScale s.r.o.)
| email: gorej@codescale.net
| web: http://www.codescale.net/


References
----------

 - http://github.com/CodeScaleInc/django-brevisurl
 - http://pypi.python.org/pypi/django-brevisurl/
 - http://www.codescale.net/en/community#django-brevisurl
