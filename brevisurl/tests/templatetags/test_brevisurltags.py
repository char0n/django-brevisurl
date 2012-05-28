from django.core.validators import URLValidator
from django.test import TestCase
from django.template import Template, Context

from brevisurl.models import ShortUrl


class TestShortenUrlTag(TestCase):

    def test_shorten_url_filter(self):
        original_url = 'http://www.codescale.net/'
        url = Template("""
        {% load brevisurltags %}
        {{ url|shorten_url }}
        """).render(Context({'url': original_url})).strip()
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertEqual(ShortUrl.objects.all()[0].original_url, original_url)
        self.assertRegexpMatches(url, URLValidator.regex)

    def test_shorten_url_filter_invalid_url(self):
        original_url = 'www.codescale.'
        url = Template("""
        {% load brevisurltags %}
        {{ url|shorten_url }}
        """).render(Context({'url': original_url})).strip()
        self.assertEqual(ShortUrl.objects.all().count(), 0)
        self.assertEqual(url, original_url)

    def test_absurl_tag(self):
        url = Template("""
        {% load brevisurltags %}
        {% absurl brevisurl_redirect token='12345' as brevis_url %}
        {{ brevis_url|shorten_url }}
        """).render(Context()).strip()
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        self.assertRegexpMatches(url, URLValidator.regex)