from unittest import TestCase
from flask import Flask
import urllib
import requests


app = Flask(__name__)


class TestOrganization(TestCase):
    token_user1 = "mock_user_001"
    token_user2 = "mock_user_002"

    def tearDown(self):
        # TEAR DOWN TEST
        response = Flask.clien .get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, msg="Drop database")

    def setUp(self):
        # SETUP TEST
        response = requests.get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, msg="Drop database")
        response = requests.get(url="http://localhost:5000/setup")
        self.assertEqual(response.status_code, 200, msg="Setup database")
        response = requests.post(url="http://localhost:5000/me",
                                 headers={'Authorization': 'Token  ' +
                                                           self.token_user1})
        self.assertEqual(response.status_code, 200, msg="User registered!")
        response = requests.post(url="http://localhost:5000/me",
                                 headers={'Authorization': 'Token  ' +
                                                           self.token_user2})
        self.assertEqual(response.status_code, 200, msg="User2 registered!")
