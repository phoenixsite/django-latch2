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
    failures = 0

    for test_suite in ["base_authentication", "allauth_authentication"]:
        os.environ["DJANGO_SETTINGS_MODULE"] = f"{test_suite}.test_settings"
        django.setup()
        TestRunner = get_runner(settings)
        test_runner = TestRunner(exclude_tags=["end-to-end"])
        failures += test_runner.run_tests([f"tests.{test_suite}"])

    sys.exit(bool(failures))
