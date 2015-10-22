"""
Test helpers.
These utilities are meant to simplify our tests, and abstract away common test
operations.
"""

from os import environ
from unittest import TestCase
from views import app
from stormpath.client import Client


class PhotogTestCase(TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['STORMPATH_APPLICATION'] = 'photog_test'
        self.app = app
        self.client = app.test_client()

        # stormpath client
        self.sp_client = Client(
            id=environ.get('STORMPATH_API_KEY_ID'),
            secret=environ.get('STORMPATH_API_KEY_SECRET'),
        )

        # # retrieve application
        href = 'https://api.stormpath.com/v1/applications/Nq2qQQegOh9a9qJRekxeA'
        self.application = self.sp_client.applications.get(href)

    def tearDown(self):
        accounts = self.application.accounts.search({
            'email': 'testuser@photog.com'
        })
        href = ""
        for account in accounts:
            if account.email == 'testuser@photog.com':
                href = account.href
                test_user = self.sp_client.accounts.get(href)
                test_user.delete()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
