from unittest import TestCase
from swarm_intelligence_app.resources.user import User
from flask import Flask, json_available
import httplib2
import urllib
import json
import requests
import jsonschema
from jsonschema import validate

app = Flask(__name__)


class TestUser(TestCase):
    token = "mock_user_001"

    def encode_param(self, firstname, lastname, email):
        params = urllib.parse.urlencode({'firstname': firstname,
                                         'lastname': lastname,
                                         'email': email})

        return params

    # def test_delete_user(self):
    #     conn = httplib2.Http(".cache")
    #     (response, content) = conn.request("http://localhost:5000/drop", "GET")
    #     self.assertEqual(response.status, 200, "drop database")
    #     (response, content) = conn.request("http://localhost:5000/setup",
    #                                        "GET")
    #     self.assertEqual(response.status, 200, "setup database")
    #     (response, content) = conn.request(
    #         uri="http://localhost:5000/users",
    #         method="POST",
    #         headers={'Content-Type': 'application/x-www-form-urlencoded'},
    #         body=TestUser.encode_param(
    #             self, 'testName', 'testLastName', 'testEmail'))
    #     self.assertEqual(response.status, 200)
    #     (response, content) = conn.request("http://localhost:5000/users/1",
    #                                        "DELETE")
    #     self.assertEqual(response.status, 200)
    #
    #     (response, content) = conn.request("http://localhost:5000/users/1",
    #                                        "DELETE")
    #     self.assertEqual(response.status, 404)
    #
    # def test_get_user(self):
    #     conn = httplib2.Http(".cache")
    #     (response, content) = conn.request("http://localhost:5000/drop",
    #                                        "GET")
    #     self.assertEqual(response.status, 200, "drop database")
    #     (response, content) = conn.request("http://localhost:5000/setup",
    #                                        "GET")
    #     self.assertEqual(response.status, 200, "setup database")
    #     (response, content) = conn.request(
    #          uri="http://localhost:5000/users",
    #          method="POST",
    #          headers={'Content-Type': 'application/x-www-form-urlencoded'},
    #          body=TestUser.encode_param(self, 'testName', 'testLastName',
    #                                     'testEmail'))
    #     self.assertEqual(response.status, 200)
    #     (response, content) = conn.request("http://localhost:5000/me",
    #                                        "GET")
    #     self.assertEqual(response.status, 200)
    #
    #     assert "1" in str(content)
    #     assert "testName" in str(content)
    #     assert "testLastName" in str(content)
    #     assert "testEmail" in str(content)
    #
    #     (response, content) = conn.request("http://localhost:5000/drop",
    #                                        "GET")
    #     self.assertEqual(response.status, 200, "drop database")
    #
    def test_update_user(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop",
                                           "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")

        (response, content) = conn.request(
            uri="http://localhost:5000/me",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'Authorization': 'Token ' + self.token})

        self.assertEqual(response.status, 200)

        # userName = content['firstname']
        #    userLastName = content['lastname']
        #    userEmail = content['email']
        # print("userName= " + userName)

        print("==========================================")
        jsonResponse = requests.request(
            method='GET',
            url="http://localhost:5000/me",
            headers={'Authorization': 'Token ' + self.token}).json()[
            'data']

        firstName = jsonResponse['firstname']
        lastName = jsonResponse['lastname']
        email = jsonResponse['email']
        id = jsonResponse['google_id']


        print(firstName + lastName + email + id)
        print("==========================================")

        # self.assertNotEquals(userName,content['firstname'])
        # self.assertNotEquals(userLastName, content['lastname'])
        # self.assertNotEquals(userEmail, content['email'])

        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")

    def test_post_users(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")

        (response, content) = conn.request(
            uri="http://localhost:5000/me",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'Authorization': 'Token ' + self.token})
        self.assertEqual(response.status, 200)

        print("content= " + str(content))

        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")
