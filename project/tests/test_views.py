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
            'login': 'caseym@gmail.com',
            'password': 'Wild94.9',
        }, follow_redirects=True)
        assert 'Dashboard' and 'caseym@gmail.com' in resp.data

        resp = self.app.post('/register', data={
            'email': 'cdm@hotmail.com',
            'password': 'Whatisthis334',
            'password_again': 'Whatisthis334',
            }, follow_redirects=True)
        # print resp.data
        assert 'Dashboard' and 'cdm@hotmail.com' in resp.data
