from unittest import TestCase
from flask import Flask
import urllib
import requests
import unittest

app = Flask(__name__)


class TestUser(TestCase):
    token = "mock_user_001"
    changeToken = "mock_user_002"

    def encode_param(self, firstname, lastname, email):
        params = urllib.parse.urlencode({'firstname': firstname,
                                         'lastname': lastname,
                                         'email': email})

        return params

    def tearDown(self):
        response = requests.get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, "drop database")

    def setUp(self):
        response = requests.get(url="http://localhost:5000/drop")
        self.assertEqual(response.status_code, 200, "drop database")
        response = requests.get(url="http://localhost:5000/setup")
        self.assertEqual(response.status_code, 200, "setup database")

    def test_delete_user(self):
        # Post Request Execution
        json_post_response = requests.request(
            method='POST',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()['data']

        first_name_post = json_post_response['firstname']
        last_name_post = json_post_response['lastname']
        email_post = json_post_response['email']
        is_deleted = json_post_response['is_deleted']

        self.assertFalse(is_deleted)
        #
        #  Delete Request Execution

        requests.delete(url="http://localhost:5000/me",
                        headers={'Authorization': 'Token ' + self.token})

        json_get_response = requests.request(
            method='GET',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()['data']

        first_name_get = json_get_response['firstname']
        last_name_get = json_get_response['lastname']
        email_get = json_get_response['email']
        is_deleted_get = json_get_response['is_deleted']

        self.assertEqual(first_name_post, first_name_get)
        self.assertEqual(last_name_post, last_name_get)
        self.assertEqual(email_post, email_get)
        self.assertTrue(is_deleted_get)

    def test_update_user(self):
        # POST Request Execution
        json_post_response = requests.request(
            method='POST',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()['data']

        first_name_post = json_post_response['firstname']
        last_name_post = json_post_response['lastname']
        email_post = json_post_response['email']

        # PUT Request Execution
        json_put_response = requests.request(
            method='PUT',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token},
            params={'firstname': 'Daisy',
                    'lastname': 'Ducks',
                    'email': 'daisy@tolli.com'}
        ).json()['data']

        first_name_put = json_put_response['firstname']
        last_name_put = json_put_response['lastname']
        email_put = json_put_response['email']
        id_put = json_put_response['google_id']

        # ASSERTION Block POST&PUT
        self.assertNotEqual(first_name_post, first_name_put)
        self.assertNotEqual(last_name_post, last_name_put)
        self.assertNotEqual(email_post, email_put)

        # GET Request Execution
        json_response = requests.request(
            method='GET',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()[
            'data']

        first_name = json_response['firstname']
        last_name = json_response['lastname']
        email = json_response['email']
        id = json_response['google_id']

        # ASSERTION Block PUT&GET
        self.assertEqual(first_name_put, first_name)
        self.assertEqual(last_name_put, last_name)
        self.assertEqual(email_put, email)
        self.assertEqual(id_put, id)

    def test_post_users(self):
        # POST Request Execution
        json_post_response = requests.request(
            method='POST',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()['data']

        first_name_post = json_post_response['firstname']
        last_name_post = json_post_response['lastname']
        email_post = json_post_response['email']
        id_post = json_post_response['google_id']

        # GET Request Execution
        json_response = requests.request(
            method='GET',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()[
            'data']

        first_name = json_response['firstname']
        last_name = json_response['lastname']
        email = json_response['email']
        id = json_response['google_id']

        # ASSERT Block
        self.assertEqual(first_name_post, first_name)
        self.assertEqual(last_name_post, last_name)
        self.assertEqual(email_post, email)
        self.assertEqual(id_post, id)


if __name__ == "__main__":
    unittest.main()
