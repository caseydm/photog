"""
Test helpers.
These utilities are meant to simplify our tests, and abstract away common test
operations.
"""

from unittest import TestCase
from views import app


class PhotogTestCase(TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass
