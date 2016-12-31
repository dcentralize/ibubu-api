"""
Test user api-functionality.

"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.user_tests import test_me
from swarm_intelligence_app.tests.circle_tests import test_circle
from swarm_intelligence_app.tests.partner_tests import test_partners


class TestRole:
    """
    Class for testing user api-functionality.

    """
    user = test_me.TestUser
    partner = test_partners.TestPartners
    circle = test_circle.TestCircle
    helper = test_helper.TestHelper
    tokens = authentication.get_mock_user()

    def test_role(self, client):
        """
        Set Up Database and run with given mock token.

        """
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)

            jwt_token = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwt_token)

            id = self.circle.get_organization_id(test_circle, client,
                                                 jwt_token)
            partner_id = self.partner.get_organization_members_id(
                test_partners, client, jwt_token, id)

            circle_id = self.circle.get_circle_id(test_circle, client,
                                                  jwt_token, id)
            role_id = self.circle.get_role_id(test_circle, client, jwt_token,
                                              circle_id)

            self.get_role(client, role_id, jwt_token)
            self.put_role(client, role_id, jwt_token)
            self.get_role_members(client, role_id, jwt_token)
            self.put_role_members_partner(client, role_id, partner_id,
                                          token)
            self.post_role_domains(client, role_id, jwt_token)
            self.get_role_domain(client, role_id, jwt_token)

            self.post_role_accountabilities(client, role_id, jwt_token)
            self.get_role_accountabilities(client, role_id, jwt_token)

            self.put_role_circle(client, role_id, jwt_token)
            self.delete_role_circle(client, role_id, jwt_token)

            self.delete_role(client, role_id, jwt_token)

    def get_role(self, client, role_id, token):
        """
        Test if the get request gets executed.

        """
        assert client.get('/roles/' + role_id,
                          headers={'Authorization': 'Bearer ' + token}
                          ).status == '200 OK'

    def put_role(self, client, role_id, token):
        """
        Test if the put request gets executed.

        """
        assert client.put('/roles/' + role_id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'name': 'New RoleName',
                                'purpose': 'New '
                                           'RolePurpose'}).status == '200 OK'

    def delete_role(self, client, role_id, token):
        """
        Test if the delete request gets executed.

        """
        assert client.delete('/roles/' + role_id,
                             headers={
                                 'Authorization': 'Bearer ' + token}) \
                   .status == '204 NO CONTENT'

    def get_role_members(self, client, role_id, token):
        """
        Test if the get request gets executed.

        """
        assert client.get('/roles/' + role_id + 'members',
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '200 OK'

    def put_role_members_partner(self, client, role_id, partner_id, token):
        """
        Test if put request gets executed.

        """
        assert client.put('/roles/' + role_id + '/members/' + partner_id,
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '204 ' \
                                                                      'NO ' \
                                                                      'CONTENT'

    def post_role_domains(self, client, role_id, token):
        """
        Test if the post request gets executed.

        """
        assert client.post('/roles/' + role_id + '/domains',
                           headers={'Authorization': 'Bearer ' +
                                                     token},
                           data={'title': 'Test Domain'}).status == '200 OK'

    def get_role_domain(self, client, role_id, token):
        """
        Test if the get request gets executed.

        """
        assert client.get('/roles/' + role_id + '/domains',
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '200 OK'

    def post_role_accountabilities(self, client, role_id, token):
        """
        Test if the post request gets executed.

        """
        assert client.post('/roles/' + role_id + '/accountabilities',
                           headers={'Authorization': 'Bearer ' +
                                                     token},
                           data={'title': 'Test Accountability'}).status == \
               '201 CREATED'

    def get_role_accountabilities(self, client, role_id, token):
        """
        Test if the get request gets executed.

        """
        assert client.get('/roles/' + role_id + '/accountabilities',
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '200 OK'

    def put_role_circle(self, client, role_id, token):
        """
        Test if the post request gets executed.

        """
        assert client.put('/roles/' + role_id + '/circle',
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '204 ' \
                                                                      'NO ' \
                                                                      'CONTENT'

    def delete_role_circle(self, client, role_id, token):
        """
        Test if the delete request gets executed.

        """
        assert client.delete('/roles/' + role_id + '/circle',
                             headers={'Authorization': 'Bearer '
                                                       '' + token}).status == \
               '204 NO CONTENT'
