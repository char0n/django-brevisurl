from django.utils import unittest
from django.contrib.sites.models import Site

from brevisurl.utils import load_object, absurl, url_has_protocol, url_has_path
from brevisurl.backends.local import BrevisUrlBackend


class TestLoadObject(unittest.TestCase):

    def test_load_valid_object(self):
        klass = load_object('brevisurl.backends.local.BrevisUrlBackend')
        self.assertEqual(klass, BrevisUrlBackend)

    def test_load_import_error(self):
        with self.assertRaises(ImportError):
            load_object('brevisurl.local.BrevisUrlBackend')

    def test_load_attribute_error(self):
        with self.assertRaises(AttributeError):
            load_object('brevisurl.backends.local.NonExistingBackend')

    def test_load_value_error(self):
        with self.assertRaises(ValueError):
            load_object('brevisurl')


class TestAbsUrl(unittest.TestCase):

    def test_protocol(self):
        abs_url = absurl(protocol='http', domain='www.codescale.net', path='/')
        self.assertEqual(abs_url, 'http://www.codescale.net/')
        abs_url = absurl(protocol='https', domain='www.codescale.net', path='/')
        self.assertEqual(abs_url, 'https://www.codescale.net/')

    def test_domain(self):
        abs_url = absurl(protocol='http', domain='www.codescale.net', path='/')
        self.assertEqual(abs_url, 'http://www.codescale.net/')
        abs_url = absurl(protocol='http', domain='sub.codescale.net', path='/')
        self.assertEqual(abs_url, 'http://sub.codescale.net/')

    def test_site(self):
        site = Site(domain='www.codescale.net', name='CodeScale.net')
        abs_url = absurl(protocol='http', site=site, path='/')
        self.assertEqual(abs_url, 'http://www.codescale.net/')

    def test_no_site_no_domain(self):
        abs_url = absurl(protocol='http', path='/')
        current_site = Site.objects.get_current()
        self.assertEqual(abs_url, 'http://' + current_site.domain + '/')

    def test_site_and_domain(self):
        site = Site(domain='www.codescale.net', name='CodeScale.net')
        abs_url = absurl(protocol='http', domain='sub.codescale.net', site=site, path='/')
        self.assertEqual(abs_url, 'http://sub.codescale.net/')


class TestUrlHasProtocol(unittest.TestCase):

    def test_url_with_protocol(self):
        url = 'http://test.sk'
        self.assertTrue(url_has_protocol(url))

    def test_url_without_protocol(self):
        url = 'test.sk/path/'
        self.assertFalse(url_has_protocol(url))


class TestUrlHasPath(unittest.TestCase):

    def test_url_with_path(self):
        url = 'http://test.sk/'
        self.assertTrue(url_has_path(url))

    def test_url_without_path(self):
        url = 'http://test.sk'
        self.assertFalse(url_has_path(url))