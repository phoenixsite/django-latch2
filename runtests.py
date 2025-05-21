"""
Test runner script
"""

# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    sys.path.append("tests")
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(exclude_tags=["end-to-end"])
    failures = test_runner.run_tests(["tests"])

    sys.exit(bool(failures))
