from unittest import TestCase
from flask import Flask, url_for
import urllib
import requests

#app = Flask(__name__)


class TestOrganization:
    token_user1 = "mock_user_001"
    token_user2 = "mock_user_002"

    # def tearDown(self, client):
    # TEAR DOWN TEST
    # response = client.get(url="http://localhost:5432/drop")
    # self.assertEqual(response.status_code, 200, msg="Drop database")

    def setUp(self, client):
        # SETUP TEST
        assert client.get(url_for('setup')).status == '200 OK'

    def test(self, client):
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
