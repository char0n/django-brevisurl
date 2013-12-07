#!/usr/bin/env python
import os
import sys
from subprocess import call


if __name__ == "__main__":
    call("./scripts/setup.sh")
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
