#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
from django.conf import settings
from django.test.utils import get_runner


def runtests():
    try:
        django.setup()
    except AttributeError:
        pass
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["brevisurl"])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
