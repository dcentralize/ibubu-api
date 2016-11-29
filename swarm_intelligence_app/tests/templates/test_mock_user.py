"""
Test user api-functionality.
"""
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from flask import json


class TestUser:
    """
    Class for testing user api-functionality.

    """
    mock_user_list = authentication.get_mock_user()
    helper = test_helper.TestHelper

    def test_me_all_users(self, client):
        self.helper.set_up(test_helper, client)
        for mock_user in self.mock_user_list:
            self.me_post(client, mock_user)


    def me_post(self, client, token):
        """
        Test if the me-page returns a valid http status-code when posting.
        """

        assert client.post('/me', headers={
            'Authorization': 'Token ' + token}).status == '200 OK'

        print('Passed test for creating a new user: ' + token)

    # def me_get(self, client, token):
    #     """
    #     Test if the get request returns the correct user.
    #     """
    #
    #     assert client.get('/me', headers={
    #         'Authorization': 'Token ' + token}).status == '200 OK'
    #     for tokens in self.mock_user_list:
    #         responseToken = client.get('/me', headers={
    #             'Authorization': 'Token ' + tokens}).json['data']
    #     print(responseToken)
