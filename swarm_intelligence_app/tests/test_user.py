import pytest

from flask import request, url_for


class TestFixtures:
    def test_client(self, client):
        assert client.get(url_for('signin')).status == '200 OK'
    token = 'mock_user_001'

    def test_db(self, client):
        assert client.get(url_for('setup')).status == '200 OK'

    def test_post(self, client):
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
