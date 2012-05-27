from django.utils import unittest

from brevisurl.utils import load_object
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