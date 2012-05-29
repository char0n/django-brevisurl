from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.validators import URLValidator

import brevisurl.settings
from brevisurl import get_connection
from brevisurl.models import ShortUrl


class TestLocalBrevisUrlBackend(TestCase):

    def setUp(self):
        self.connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')

    def test_shorten_url_use_site_framework(self):
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = None
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        original_url = 'http://www.codescale.net/'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, URLValidator.regex)

    def test_shorten_url_domain_from_settings(self):
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = 'http://brevisurl.net/'
        original_url = 'http://www.codescale.net/'
        short_url = self.connection.shorten_url(original_url)
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(short_url.original_url, original_url)
        self.assertRegexpMatches(short_url.shortened_url, r'^http://brevisurl\.net/[a-zA-Z0-9]{5}$')

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