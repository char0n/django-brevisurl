from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

import brevisurl.settings
from brevisurl import get_connection
from brevisurl.models import ShortUrl


class TestBrevisUrlRedirectView(TestCase):

    def setUp(self):
        self.LOCAL_BACKEND_DOMAIN = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = None
        self.site = Site.objects.get_current()
        self.connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
        self.short_url = ShortUrl()
        self.short_url.original_url = 'http://www.codescale.net/'
        self.short_url.shortened_url = '{0}://{1}/12345'.format(brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL,
                                                                self.site.domain)
        self.short_url.backend = self.connection.class_path
        self.short_url.save()
        self.client = Client()

    def tearDown(self):
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = self.LOCAL_BACKEND_DOMAIN

    def test_redirect(self):
        response = self.client.get(reverse('brevisurl_redirect', kwargs={'token': 12345}))
        self.assertEqual(response.status_code, 301)

    def test_redirect_non_existing_token(self):
        response = self.client.get(reverse('brevisurl_redirect', kwargs={'token': 54321}))
        self.assertEqual(response.status_code, 404)