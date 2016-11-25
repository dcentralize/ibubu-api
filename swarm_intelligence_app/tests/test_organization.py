"""
Test user api-functionality.
"""
from swarm_intelligence_app.tests import test_helper


class TestOrganization:
    """
    Class for testing user api-functionality.

    """
    helper = test_helper.TestHelper

    token = 'mock_user_001'

    def test_me_post(self, client):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        self.helper.set_up(test_helper, client)
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
        print('Passed test for creating a new user.')
