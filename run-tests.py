#!/usr/bin/env python
import sys
import os
import unittest

if len(sys.argv) <= 1:
    print "Usage: ./test-runner.py <test_name>"
    sys.exit(1)


# to keep Django quiet
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


current_dir = os.path.dirname(__file__)
suites = []
loader = unittest.TestLoader()
for test_name in sys.argv[1:]:
    test_prefix = 'tests.%s' % test_name
    exec('from %s import get_suites' % test_prefix);
    suites.append(get_suites())

unittest.TextTestRunner().run(unittest.TestSuite(suites))

