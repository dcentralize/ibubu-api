"""
Test user api-functionality.

"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.circle_tests import test_circle
from swarm_intelligence_app.tests.user_tests import test_me


class TestCircle:
    """
    Class for testing user api-functionality.

    """
    user = test_me.TestUser
    helper = test_helper.TestHelper
    circle = test_circle.TestCircle
    tokens = authentication.get_mock_user()

    def test_organization(self, client):
        """
        Set up Database and run with given mock tokens.

        """
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwt_token)
            id = self.circle.get_organization_id(test_circle, client,
                                                 jwt_token)
            circle_id = self.circle.get_circle_id(test_circle, client,
                                                  jwt_token,
                                                  id)
            id_partner = self.circle.get_partner_id(test_circle, client, id,
                                                    jwt_token)
            role_id = self.circle.get_role_id(test_circle, client, jwt_token,
                                              circle_id)

            self.circle_get_no_login(client, circle_id)
            self.circle_put_no_login(client, circle_id)
            self.circle_put_no_param(client, circle_id, jwt_token)
            self.circle_put_wrong_param(client, circle_id, jwt_token)
            self.circle_post_roles_no_login(client, circle_id)
            self.circle_post_roles_no_param(client, circle_id, jwt_token)
            self.circle_post_roles_wrong_param(client, circle_id, jwt_token)
            self.circle_get_roles_no_login(client, circle_id)
            self.circle_put_subcircles_no_login(client, role_id)
            self.circle_put_subcircles_no_param(client, circle_id, jwt_token)
            self.circle_put_subcircles_wrong_param(client, circle_id,
                                                   jwt_token)
            self.circle_get_subcircles_no_login(client, circle_id)
            self.circle_get_members_no_login(client, circle_id)
            self.circle_put_partner_no_login(client, circle_id, id_partner)
            self.circle_delete_partner_no_login(client, circle_id, id_partner)

    def circle_get_no_login(self, client, circle_id):
        """
        Test if the get requests without a valid token returns a 400 status
        code.

        """
        assert client.get('/circles/' + circle_id).status == '400 BAD REQUEST'

    def circle_put_no_login(self, client, circle_id):
        """
        Test if the put request without a valid token returns a 400 status
        code.

        """
        assert client.put('/circles/' + circle_id, headers={},
                          data={'name': 'Name2',
                                'purpose': 'Purpose2',
                                'strategy': 'Strategy2'}) \
                   .status == '400 BAD REQUEST'

    def circle_put_no_param(self, client, circle_id, token):
        """
        Test if the put request with a missing body returns a 400 status code.

        """
        assert client.put('/circles/' + circle_id, headers={
            'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'

    def circle_put_wrong_param(self, client, circle_id, token):
        """
        Test if the put request without a correct body returns a 400 status
        code.

        """
        assert client.put('/circles/' + circle_id, headers={
            'Authorization': 'Bearer ' + token},
                          data={'purpose': 'Purpose2',
                                'strategy': 'Strategy2'}) \
                   .status == '400 BAD REQUEST'

    def circle_post_roles_no_login(self, client, circle_id):
        """
        Test if the post request without a valid token returns a 400 status
        code.

        """
        assert client.post('/circles/' + circle_id + '/roles', headers={},
                           data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status == '400 BAD ' \
                                                                  'REQUEST'

    def circle_post_roles_no_param(self, client, circle_id, token):
        """
        Test if the post request with a missing body returns a 400 status code.

        """
        assert client.post('/circles/' + circle_id + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={}).status == '400 BAD REQUEST'

    def circle_post_roles_wrong_param(self, client, circle_id, token):
        """
        Test if the post request without a correct body returns a 400 status
        code.

        """
        assert client.post('/circles/' + circle_id + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status == '400 BAD ' \
                                                                  'REQUEST'

    def circle_get_roles_no_login(self, client, circle_id):
        """
        Test if the get request without a valid token returns a 400 status
        code.

        """
        assert client.get('/circles/' + circle_id + '/roles', headers={},
                          data={}).status == '400 BAD REQUEST'

    def circle_put_subcircles_no_login(self, client, role_id):
        """
        Test if the put request without a valid token returns a 400 status
        code.

        """
        assert client.put('/roles/' + role_id + '/circle', headers={},
                          data={'name': 'NewRole',
                                'purpose': 'This is a new Role added to a '
                                           'Circle.',
                                'strategy': 'NewStrategy'}).status == '400 ' \
                                                                      'BAD ' \
                                                                      'REQUEST'

    def circle_put_subcircles_no_param(self, client, role_id, token):
        """
        Test if the put request with a missing body returns a 400 status code.

        """
        assert client.put('/roles/' + role_id + '/circle', headers={
            'Authorization': 'Bearer ' + token},
                          data={}).status == '204 NO CONTENT'

    def circle_put_subcircles_wrong_param(self, client, role_id, token):
        """
        Test if the put request without a correct body returns a 400 status
        code.

        """
        assert client.put('/roles/' + role_id + '/circle', headers={
            'Authorization': 'Bearer ' + token},
                          data={'name': 'NewRole',
                                'strategy': 'NewStrategy'}). \
            status == '204 NO CONTENT'

    def circle_get_subcircles_no_login(self, client, role_id):
        """
        Test if the get request without a valid token returns a 400 status
        code.

        """
        assert client.put('/roles/' + role_id + '/circle', headers={
        }).status == '400 BAD REQUEST'

    def circle_get_members_no_login(self, client, circle_id):
        """
        Test if the get request without a valid token returns a 400 status
        code.

        """
        assert client.get('/circles/' + circle_id + '/members',
                          headers={}).status == '400 BAD REQUEST'

    def circle_put_partner_no_login(self, client, circle_id, id_partner):
        """
        Test if the put request without a valid token returns a 400 status
        code.

        """
        assert client.put('/circles/' + circle_id + '/members/' + id_partner,
                          headers={},
                          data={'firstname': 'Manuel', 'lastname':
                                'Neuer', 'email': 'm.neuer@mail.com'}).status\
            == '400 BAD REQUEST'

    def circle_delete_partner_no_login(self, client, circle_id, id_partner):
        """
        Test if the delete request without a valid token returns a 400 status
        code.

        """
        assert client.delete('/circles/' + circle_id + '/members/' +
                             id_partner,
                             headers={}
                             ).status == '400 BAD REQUEST'
