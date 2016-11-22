from unittest import TestCase
from flask import Flask
import urllib
import requests

app = Flask(__name__)


class TestOrganization(TestCase):
    token = "mock_user_001"

    def tearDown(self):
        # TEAR DOWN TEST
        response = requests.get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, msg="Drop database")

    def setUp(self):
        # SETUP TEST
        response = requests.get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, msg="Drop database")
        response = requests.get(url="http://localhost:5000/setup")
        self.assertEqual(response.status_code, 200, msg="Setup database")
        response = requests.post(url="http://localhost:5000/me",
                                 headers={'Authorization': 'Token  ' +
                                                           self.token})
        self.assertEqual(response.status_code, 200, msg="User registered!")

    def test_get_organization(self):
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        success_json = response_json['success']
        self.assertTrue(success_json, msg="Success is true")

    def test_post_organization(self):
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['data']
        self.assertEqual(len(response_json), 0, msg="Array should be empty")
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token})

        response_json = response.json()['data']
        self.assertEqual(len(response_json), 1, msg="Array should has one "
                                                    "entry")
        self.assertEqual(response_json[0]['name'], 'Test-Organization')
        self.assertTrue(response.json()['success'])
        self.assertFalse(response_json[0]['is_deleted'])

    def test_delete_organization(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token})
        self.assertFalse(response.json()['data'][0]['is_deleted'])
        response = requests.delete(
            url="http://localhost:5000/organizations/1",
            headers={'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorizations': 'Token ' +
                                                           self.token})
        self.assertTrue(response.json()['data'][0]['is_deleted'])

    def test_change_name(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={
                                    'Authorization': 'Token ' + self.token})
        self.assertEqual(response.json()['data'][0]['name'],
                         'Test-Organization')
        response = requests.put(url="http://localhost:5000/organizations/1",
                                headers={'Authorization': 'Token ' +
                                                          self.token},
                                params={'name': 'ChangeNameOrganization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={
                                    'Authorization': 'Token ' + self.token})

        self.assertEqual(response.json()['data'][0]['name'],
                         'ChangeNameOrganization')
        self.assertEqual(response.json()['data'][0]['id'], 1)
        self.assertFalse(response.json()['data'][0]['is_deleted'])
        self.assertTrue(response.json()['success'])