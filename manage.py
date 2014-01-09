#!/usr/bin/env python
import os
import sys

sys.path.append("C:\\Users\Code\Baros")
os.environ['DJANGO_SETTINGS_MODULE'] = 'baros.settings'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baros.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
