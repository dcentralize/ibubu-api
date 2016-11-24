"""
Class for testing user api-functionality.

"""
from flask import url_for


class TestFixtures:
    token = 'mock_user_001'

    def test_client(self, client):
        """
        Tests if the signin-page returns a valid http status-code
        """
        assert client.get(url_for('signin')).status == '200 OK'

    def test_db(self, client):
        """
        Tests if the setup-page returns a valid http status-code
        """
        assert client.get(url_for('setup')).status == '200 OK'

    def test_post(self, client):
        """
        Tests if the me-page returns a valid http status-code
        """
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
