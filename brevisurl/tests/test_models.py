from random import sample

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.sites.models import Site

import brevisurl.settings
from brevisurl.models import ShortUrl
from brevisurl import get_connection

def _random_string(k):
    """Generate a string of length k ascii letters randomly"""
    return ''.join(random.choice(string.ascii_letters) for x in xrange(k))
    

class TestModels(TestCase):

    def test_model_save(self):
        site = Site.objects.get_current()
        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
        short_url = ShortUrl()
        short_url.original_url = 'http://www.codescale.net/'
        short_url.shortened_url = '{0}://{1}/12345'.format(brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL,
                                                           site.domain)
        short_url.backend = connection.class_path
        short_url.save()
        self.assertIsNotNone(short_url.pk)

    def test_model_save_invalid_original_url(self):
        with self.assertRaises(ValidationError):
            self.site = Site.objects.get_current()
            self.connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
            self.short_url = ShortUrl()
            self.short_url.original_url = 'www.codescale{0}.' 
            self.short_url.shortened_url = '{0}://{1}/12345'.format(brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL,
                                                                    self.site.domain)
            self.short_url.backend = self.connection.class_path
            self.short_url.save()

    def test_model_save_too_long_original_url(self):
        with self.assertRaises(ValidationError):
            self.site = Site.objects.get_current()
            self.connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
            self.short_url = ShortUrl()
            self.short_url.original_url = 'www.codescale{0}.com'.format(_random_string(
                                                                     brevisurl.settings.LOCAL_BACKEND_ORIGINAL_URL_MAX_LENGTH + 1))
            self.short_url.shortened_url = '{0}://{1}/12345'.format(brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL,
                                                                    self.site.domain)
            self.short_url.backend = self.connection.class_path
            self.short_url.save()


    def test_model_save_invalid_shortened_url(self):
        with self.assertRaises(ValidationError):
            connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
            short_url = ShortUrl()
            short_url.original_url = 'http://www.codescale.net/'
            short_url.shortened_url = 'www.codescale.'
            short_url.backend = connection.class_path
            short_url.save()
