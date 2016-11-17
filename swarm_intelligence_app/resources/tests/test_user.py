from unittest import TestCase
from swarm_intelligence_app.resources.user import User
from flask import Flask
import httplib2
import urllib
import json
import jsonschema
from jsonschema import validate

app = Flask(__name__)


class TestUser(TestCase):
    def encode_param(self, firstname, lastname, email):
        params = urllib.parse.urlencode({'firstname': firstname,
                                         'lastname': lastname,
                                         'email': email})
        return params

    def test_delete_user(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")
        (response, content) = conn.request(
            uri="http://localhost:5000/users",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=TestUser.encode_param(
                self, 'testName', 'testLastName', 'testEmail'))
        self.assertEqual(response.status, 200)
        (response, content) = conn.request("http://localhost:5000/users/1",
                                           "DELETE")
        self.assertEqual(response.status, 200)

        (response, content) = conn.request("http://localhost:5000/users/1",
                                           "DELETE")
        self.assertEqual(response.status, 404)

    def test_get_user(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop",
                                           "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")
        (response, content) = conn.request(
             uri="http://localhost:5000/users",
             method="POST",
             headers={'Content-Type': 'application/x-www-form-urlencoded'},
             body=TestUser.encode_param(self, 'testName', 'testLastName',
                                        'testEmail'))
        self.assertEqual(response.status, 200)
        (response, content) = conn.request("http://localhost:5000/users/1",
                                           "GET")
        self.assertEqual(response.status, 200)

        assert "1" in str(content)
        assert "testName" in str(content)
        assert "testLastName" in str(content)
        assert "testEmail" in str(content)

        (response, content) = conn.request("http://localhost:5000/drop",
                                           "GET")
        self.assertEqual(response.status, 200, "drop database")

    def test_update_user(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop",
                                           "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")
        (response, content) = conn.request("http://localhost:5000/users",
                                           "GET")

        self.assertEqual(response.status, 200)

        (response, content) = conn.request(
            uri="http://localhost:5000/users",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=TestUser.encode_param(
                self, 'testName', 'testLastName', 'testEmail'))

        self.assertEqual(response.status, 200)

        (response, content) = conn.request(
            uri="http://localhost:5000/users/1",
            method="PUT",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=TestUser.encode_param(
                self, 'changeName', 'changeLastName', 'changeEmail@hh.de'))

        self.assertEqual(response.status, 200)
        (response, content) = conn.request("http://localhost:5000/users/1",
                                           "GET")

        assert "changeName" in str(content)
        assert "changeLastName" in str(content)
        assert "changeEmail@hh.de" in str(content)

        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")

    def test_post_users(self):
        conn = httplib2.Http(".cache")
        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")
        (response, content) = conn.request("http://localhost:5000/setup",
                                           "GET")
        self.assertEqual(response.status, 200, "setup database")
        (response, content) = conn.request("http://localhost:5000/users",
                                           "GET")

        self.assertEqual(response.status, 200)

        (response, content) = conn.request(
            uri="http://localhost:5000/users",
            method="POST",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=TestUser.encode_param(
                self, 'testName', 'testLastName', 'testEmail'))
        self.assertEqual(response.status, 200)

        (response, content) = conn.request("http://localhost:5000/users",
                                           "GET")
        self.assertEqual(response.status, 200)
        assert 'testName' in str(content)
        assert 'testLastName' in str(content)
        assert 'testEmail' in str(content)

        (response, content) = conn.request("http://localhost:5000/drop", "GET")
        self.assertEqual(response.status, 200, "drop database")
