from django.utils import unittest

from brevisurl import get_connection, shorten_url
from brevisurl.backends.local import BrevisUrlBackend
from brevisurl.backends.base import BaseBrevisUrlBackend


class TestGetConnection(unittest.TestCase):

    def test_get_default_connection(self):
        connection = get_connection()
        self.assertIsInstance(connection, BrevisUrlBackend)

    def test_get_custom_connection(self):
        base_connection = get_connection(backend='brevisurl.backends.base.BaseBrevisUrlBackend')
        local_connection = get_connection(backend='brevisurl.backends.local.BrevisUrlBackend')
        self.assertIsInstance(base_connection, BaseBrevisUrlBackend)
        self.assertIsInstance(local_connection, BrevisUrlBackend)

    def test_get_connection_non_existing_backend(self):
        with self.assertRaises(AttributeError):
            get_connection(backend='brevisurl.backends.local.NonExistingBackend')