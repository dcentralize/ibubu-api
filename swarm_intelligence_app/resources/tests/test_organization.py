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
                                                           self.token_user1})
        self.assertEqual(response.status_code, 200, msg="User registered!")
        response = requests.post(url="http://localhost:5000/me",
                                 headers={'Authorization': 'Token  ' +
                                                           self.token_user2})
        self.assertEqual(response.status_code, 200, msg="User2 registered!")

    def test_get_organization(self):
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        success_json = response_json['success']
        self.assertTrue(success_json, msg="Success is true")

    def test_post_organization(self):
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['data']
        self.assertEqual(len(response_json), 0, msg="Array should be empty")
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})

        response_json = response.json()['data']
        self.assertEqual(len(response_json), 1, msg="Array should has one "
                                                    "entry")
        self.assertEqual(response_json[0]['name'], 'Test-Organization')
        self.assertTrue(response.json()['success'])
        self.assertFalse(response_json[0]['is_deleted'])

    def test_delete_organization(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})
        self.assertFalse(response.json()['data'][0]['is_deleted'])
        response = requests.delete(
            url="http://localhost:5000/organizations/1",
            headers={'Authorization': 'Token ' + self.token_user1})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})

        self.assertEqual(len(response.json()['data']), 0, msg="Array should "
                                                              "be empty")
        response = requests.get(url="http://localhost:5000/organizations/1",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1})

        self.assertTrue(response.json()['data']['is_deleted'])

    def test_change_name(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={
                                    'Authorization': 'Token ' +
                                                     self.token_user1})
        self.assertEqual(response.json()['data'][0]['name'],
                         'Test-Organization')
        response = requests.put(url="http://localhost:5000/organizations/1",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1},
                                params={'name': 'ChangeNameOrganization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(url="http://localhost:5000/me/organizations",
                                headers={
                                    'Authorization': 'Token ' +
                                                     self.token_user1})

        self.assertEqual(response.json()['data'][0]['name'],
                         'ChangeNameOrganization')
        self.assertEqual(response.json()['data'][0]['id'], 1)
        self.assertFalse(response.json()['data'][0]['is_deleted'])
        self.assertTrue(response.json()['success'])

    def test_get_member(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            url="http://localhost:5000/organizations/1/members",
            headers={'Authorization': 'Token ' + self.token_user1})

        self.assertEqual(len(response.json()['data']), 1,
                         msg="One member is assigned")

        json_get_user = requests.get(
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token_user1}).json()[
            'data']

        first_name_get = json_get_user['firstname']
        last_name_get = json_get_user['lastname']
        email_get = json_get_user['email']

        self.assertEqual(first_name_get, response.json()['data'][0][
            'firstname'])
        self.assertEqual(last_name_get, response.json()['data'][0][
            'lastname'])
        self.assertEqual(email_get, response.json()['data'][0][
            'email'])
        self.assertFalse(response.json()['data'][0]['is_deleted'])

    def test_get_admin(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            url="http://localhost:5000/organizations/1/admins",
            headers={'Authorization': 'Token ' + self.token_user1})

        json_get_user = requests.get(
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token_user1}).json()[
            'data']

        first_name_get = json_get_user['firstname']
        last_name_get = json_get_user['lastname']
        email_get = json_get_user['email']

        self.assertEqual(first_name_get, response.json()['data'][0][
            'firstname'])
        self.assertEqual(last_name_get, response.json()['data'][0][
            'lastname'])
        self.assertEqual(email_get, response.json()['data'][0][
            'email'])
        self.assertFalse(response.json()['data'][0]['is_deleted'])

        self.assertEqual(response.json()['data'][0]['email'], email_get)
        self.assertEqual(response.json()['data'][0]['firstname'],
                         first_name_get)
        self.assertEqual(response.json()['data'][0]['lastname'], last_name_get)
        self.assertEqual(response.json()['data'][0]['type'], 'admin')
        self.assertTrue(response.json()['success'])
        self.assertEqual(len(response.json()['data']), 1, msg="Only one "
                                                              "admin")

    # Organization Invitations

    def test_send_invitation(self):
        response = requests.post(url="http://localhost:5000/me/organizations",
                                 headers={'Authorization': 'Token ' +
                                                           self.token_user1},
                                 params={'name': 'Test-Organization'})
        self.assertEqual(response.status_code, 200)
        response = requests.post(
            url="http://localhost:5000/organizations/1/invitations",
            headers={'Authorization': 'Token ' + self.token_user1},
            params={'email': 'dagobert@gmail.de'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('dagobert@gmail.de', response.json()['data']['email'])
        invitationCode = response.json()['data']['code']
        response = requests.get(
            url="http://localhost:5000/invitations/" + invitationCode +
                "/accept",
            headers={'Authorization': 'Token ' + self.token_user2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['status'], "accepted")
        self.assertEqual(response.json()['data']['code'], invitationCode)
