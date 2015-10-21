"""Run tests against our custom views."""

from test_helpers import PhotogTestCase


class TestRegister(PhotogTestCase):
    """Test our registration view."""

    def test_register_user(self):
        # Page loads with correct text
        resp = self.app.get('/register')
        assert 'Register for an Account' in resp.data

        # Ensure that no password results in error
        resp = self.app.post('/register', data={
            'email': 'cdm@hotmail.com',
            'password': '',
            'password_again': '',
            })
        assert 'Register for an Account' in resp.data

        # Ensure that no email address results in error
        resp = self.app.post('/register', data={
            'email': '',
            'password': 'TempPass123',
            'password_again': 'TempPass123',
            })
        print resp.data
        assert 'Register for an Account' in resp.data

        # Valid data results in success
        resp = self.app.post('/register', data={
            'email': 'testuser@photog.com',
            'password': 'TempPass123',
            'password_again': 'TempPass123',
            }, follow_redirects=True)
        print resp.data
        assert 'Dashboard' in resp.data


class TestLogin(PhotogTestCase):
    """Test login view."""

    # Page loads with correct text
    def test_login_user(self):
        resp = self.app.get('/login')
        assert 'Log in to your Account' in resp.data



