"""
Use for Setting Up tests.
"""
import json

from flask import url_for


class TestHelper:
    """
    Class for cleaning the database for each test.
    """

    def test_setup(self, client):
        """
        Test if the setup-page returns a valid http status-code.
        """
        assert client.get(url_for('setup')).status == '200 OK'
        print('Passed test for setup.')

    def test_populate(self, client):
        """
        Test if the populate-page returns a valid http status-code.
        """
        assert client.get(url_for('populate')).status == '200 OK'
        print('Passed test for populating the database.')

    def signin(self, client):
        """
        Helper Method for populating the database.
        """
        client.get(url_for('signin'))

    def set_up(self, client):
        """
        Helper method for setting up the database.
        """
        client.get(url_for('setup'))

    def populate(self, client):
        """
        Helper Method for populating the database.
        """
        client.get(url_for('populate'))

    def login(self, client, token):
        """
        Helper Method for loggin in.
        """
        response = client.get('/login', headers={
            'Authorization': 'Token ' + token})

        json_data = response.json['data']['access_token']
        return json_data
