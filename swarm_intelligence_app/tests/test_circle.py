from unittest import TestCase
from flask import Flask, url_for, jsonify
import urllib
import requests
import json


# app = Flask(__name__)


class TestCircle:
    token_user1 = "mock_user_001"
    token_user2 = "mock_user_002"

    def setUp(self, client):
        assert client.get(url_for('setup')).status == '200 OK'

        assert client.post("/me", headers={
            'Authorization': 'Token  ' + self.token_user1}).status == '200 OK'

        assert client.post("/me", headers={
            'Authorization': 'Token  ' + self.token_user2}).status == '200 OK'
        assert client.post("/me/organizations",
                           headers={
                               'Authorization': 'Token ' + self.token_user1},
                           data={
                               'name': 'CheGuevara GmbH'}).status == '200 OK'

    def test_get_circle(self, client):
        self.setUp(client)

        assert client.get("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1}).status == '200 OK'
        assert client.get("/circles/2",
                          headers={
                              'Authorization': 'Token ' +
                                               self.token_user1}).status == \
               '404 NOT FOUND'

    def test_put_circle(self, client):
        self.setUp(client)
        assert client.put("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1},
                          data={'name': 'changeCircleName'}).status == '200 OK'

    def test_delete_circle(self, client):
        self.setUp(client)
        assert client.get("/circles/1", headers={'Authorization': 'Token ' +
                                                                  self.token_user1}).status == '200 OK'
        assert client.delete("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1}).status == '200 OK'
        assert client.get("/circles/1", headers={'Authorization': 'Token ' +
                                                                  self.token_user1}).status == '404 NOT FOUND'
