from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.validators import URLValidator

import brevisurl.settings
from brevisurl import get_connection
from brevisurl.models import ShortUrl
from brevisurl.backends.local import TokensExhaustedError


class TestLocalBrevisUrlBackend(TestCase):

    def setUp(self):
        self.connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')

    def test_shorten_url_use_site_framework(self):
        _original_domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = None
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        original_url = 'http://www.codescale.net/'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = _original_domain

    def test_shorten_url_domain_from_settings(self):
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        _original_domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = 'http://brevisurl.net/'
        original_url = 'http://www.codescale.net/'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, r'^http://brevisurl\.net/[a-zA-Z0-9]{5}$')
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = _original_domain

    def test_shorten_url_reuse_old(self):
        original_url = 'http://www.codescale.net/'
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)

    def test_shorten_url_create_new(self):
        original_url = 'http://www.codescale.net/'
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)
        original_url = 'http://www.codescale.net/en/company/'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 2)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)

    def test_shorten_url_invalid_original_url(self):
        with self.assertRaises(ValidationError):
            self.connection.shorten_url('www.codescale.')
        self.assertEqual(ShortUrl.objects.all().count(), 0)

    def test_shorten_url_invalid_original_url_fail_silently(self):
        self.connection.fail_silently = True
        shorl_url = self.connection.shorten_url('www.codescale.')
        self.assertIsNone(shorl_url)

    def test_configurable_token_chars(self):
        original_url = 'http://www.codescale.net/'
        _default_chars = brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS
        brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS = ['a']
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, r'/aaaaa$')
        brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS = _default_chars

    def test_exhausted_tokens(self):
        original_url = 'http://www.codescale.net/'
        _default_chars = brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS
        brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS = ['a']
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        with self.assertRaises(TokensExhaustedError):
            original_url = 'http://www.codescale.net/another/'
            short_url = self.connection.shorten_url(original_url)
        brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS = _default_chars

    def test_custom_domain(self):
        original_url = 'http://www.codescale.net/'
        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend', domain='http://test.com/')
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertRegexpMatches(short_url.shortened_url, r'^http://test\.com/.{5}')

    def test_configurable_protocol(self):
        _original_domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = None
        original_url = 'http://www.codescale.net/'
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertRegexpMatches(short_url.shortened_url, '^http://')
        original_url = 'http://www.codescale.net/another'
        _default_protocol = brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL
        brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL = 'https'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 2)
        self.assertRegexpMatches(short_url.shortened_url, '^https://')
        brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL = _default_protocol
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = _original_domain

    def test_url_path_slash_stripping(self):
        original_url = 'http://www.codescale.net/'
        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend', domain='http://test.com/d')
        short_url = connection.shorten_url(original_url)
        self.assertRegexpMatches(short_url.shortened_url, r'^http://test\.com/d[^/]{5}$')

    def test_url_path_slash_no_stripping(self):
        original_url = 'http://www.codescale.net/'
        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend', domain='http://test.com/d/')
        short_url = connection.shorten_url(original_url)
        self.assertRegexpMatches(short_url.shortened_url, r'^http://test\.com/d/[^/]{5}$')