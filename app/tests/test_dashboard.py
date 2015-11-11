from app import db
from test_helpers import PhotogTestCase
from app.dashboard.models import Contact


class TestAddContact(PhotogTestCase):
    """Test our add contact view."""

    def test_add_contact_page_loads(self):
        self.login(self.user.email, self.test_password)

        # Page loads with correct text
        resp = self.client.get('/newcontact', follow_redirects=True)
        assert 'Add Contact' in resp.data

    def test_add_contact_page_bad_data(self):
        self.login(self.user.email, self.test_password)

        # Return error with bad data
        resp = self.client.post('/newcontact', data={
                'name': '',
                'email': 'test@hotmail.com'
            }, follow_redirects=True)
        assert 'Add Contact' in resp.data

        resp = self.client.post('/newcontact', data={
                'name': 'Joe',
                'email': ''
            }, follow_redirects=True)
        assert 'Add Contact' in resp.data

    def test_add_contact_page_good_data(self):
        self.login(self.user.email, self.test_password)

        # New contact available on dashboard page
        new_contact = Contact(
            'Roger',
            'roger@hotmail.com',
            '234-234-2343',
            'wants a photo session',
            'Web Site',
            self.user.href,
            self.user.custom_data['tenant_id']
        )
        db.session.add(new_contact)
        db.session.commit()
        resp = self.client.get('/dashboard', follow_redirects=True)
        assert 'Roger' in resp.data
        assert 'roger@hotmail.com' in resp.data
        assert '234-234-2343'
