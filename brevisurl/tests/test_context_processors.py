from django.utils import unittest

import brevisurl.settings
from brevisurl import context_processors


class TestContextProcessors(unittest.TestCase):

    def test_context_processor_defaults(self):
        _DEFAULT_BACKEND = brevisurl.settings.DEFAULT_BACKEND
        _LOCAL_BACKEND_DOMAIN = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.DEFAULT_BACKEND = 'brevisurl.backends.local.BrevisUrlBackend'
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = None
        result = context_processors.brevisurl_data(None)
        self.assertIn('BREVIS_BACKEND', result)
        self.assertIn('BREVIS_BACKEND_LOCAL_DOMAIN', result)
        self.assertEqual(result['BREVIS_BACKEND'], 'brevisurl.backends.local.BrevisUrlBackend')
        self.assertIsNone(result['BREVIS_BACKEND_LOCAL_DOMAIN'])
        brevisurl.settings.DEFAULT_BACKEND = _DEFAULT_BACKEND
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = _LOCAL_BACKEND_DOMAIN

    def test_context_processor_custom(self):
        _DEFAULT_BACKEND = brevisurl.settings.DEFAULT_BACKEND
        _LOCAL_BACKEND_DOMAIN = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        brevisurl.settings.DEFAULT_BACKEND = 'brevisurl.backends.base.BaseBrevisUrlBackend'
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = 'http://brevisurl.net/'
        result = context_processors.brevisurl_data(None)
        self.assertIn('BREVIS_BACKEND', result)
        self.assertIn('BREVIS_BACKEND_LOCAL_DOMAIN', result)
        self.assertEqual(result['BREVIS_BACKEND'], 'brevisurl.backends.base.BaseBrevisUrlBackend')
        self.assertEqual(result['BREVIS_BACKEND_LOCAL_DOMAIN'], 'http://brevisurl.net/')
        brevisurl.settings.DEFAULT_BACKEND = _DEFAULT_BACKEND
        brevisurl.settings.LOCAL_BACKEND_DOMAIN = _LOCAL_BACKEND_DOMAIN