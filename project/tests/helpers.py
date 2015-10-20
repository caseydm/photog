"""
Test helpers.
These utilities are meant to simplify our tests, and abstract away common test
operations.
"""

from unittest import TestCase
from views import app


class PhotogTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False

    def tearDown(self):
        pass
