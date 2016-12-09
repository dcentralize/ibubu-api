"""
Use for Setting Up tests.
"""
import json

from flask import url_for

from swarm_intelligence_app.models import organization


class TestHelper:
    """
    Class for cleaning the database for each test.
    """

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

    def get_organization_id(self, client, token):
        """
        Helper Method getting an organization_id
        """
        organization_id = client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}, ).json['data']
        print(organization)
        return organization_id
