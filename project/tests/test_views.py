"""Run tests against our custom views."""

from helpers import PhotogTestCase


class TestRegister(PhotogTestCase):
    """Test our registration view."""

    def test_register_user(self):
        # Ensure page loads with correct text
        resp = self.app.get('/register')
        assert 'Register for an Account' in resp.data

        # Ensure that valid fields result in success.
        resp = self.app.post('/login', data={
            'email': 'caseym@gmail.com',
            'password': 'Wild94.9',
            #'password_again': 'woot1LoveCookies!'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 302)
