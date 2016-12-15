"""
Define Organization Exception Tests.

"""
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.user_tests import test_me
from swarm_intelligence_app.tests.organization_tests import test_organization


class TestOrganizationException:
    """
    Test API for exceptions.

    """
    helper = test_helper.TestHelper
    user = test_me.TestUser
    organization = test_organization.TestOrganization
    tokens = authentication.get_mock_user()

    def test_organization_exceptions(self, client):
        """
        Test with multiple token.

        """
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwt_token)
            id = self.organization.get_organization_id(
                test_organization,
                client, jwt_token)

            self.organization_post_not_allowed(client, id)
            self.organization_get_members_no_login(client, id)
            self.organization_get_admins_no_login(client, id)
            self.organization_post_invitation_no_login(client, id)
            self.organization_get_invitation_no_login(client, id)
            self.organization_get_no_login(client, id)
            self.organization_put_no_login(client, id)
            self.organization_put_no_param(client, jwt_token, id)
            self.organization_put_wrong_params(client, token, id)
            self.organization_del_no_login(client, id)
            self.organization_del_no_param(client, jwt_token, id)

    def organization_post_not_allowed(self, client, id):
        """
        Test if the me-page returns a valid http status-code when posting.

        """
        assert client.post(
            '/organizations/' + id).status == '405 METHOD NOT ALLOWED'

    def organization_get_no_login(self, client, id):
        """
        Test if the me-page returns a valid http status-code when getting.

        """
        assert client.get('/organizations/' + id).status == '400 BAD REQUEST'

    def organization_put_no_login(self, client, id):
        """
            Test if the me-page returns a valid http status-code when putting.

        """
        assert client.put('/organizations/' + id, headers={},
                          data={'name': 'Daisy'}).status == '400 BAD REQUEST'

    def organization_put_wrong_params(self, client, token, id):
        """
        Test if the me-page returns a valid http status-code when putting.

        """
        assert client.put('/organizations/' + id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
               '400 BAD REQUEST'

    def organization_put_no_param(self, client, token, id):
        """
        Test if the me-page returns a valid http status-code when putting.

        """
        assert client.put('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'

    def organization_del_no_login(self, client, id):
        """
        Test if the me-page returns a valid http status-code when deleting.

        """
        assert client.delete('/organizations/' + id, headers={},
                             data={'name': 'Daisy'}).status == \
               '400 BAD REQUEST'

    def organization_del_no_param(self, client, token, id):
        """
        Test if the me-page returns a valid http status-code when deleting.

        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token},
                             data={}).status == '204 NO CONTENT'

    def organization_get_members_no_login(self, client, id):
        """
        Test if the me-page returns a valid http status-code when deleting.

        """
        assert client.get('/organizations/' + id + '/members',
                          headers={}).status == '400 BAD REQUEST'

    def organization_get_admins_no_login(self, client, id):
        """
        Test if the me-page returns a valid http status-code when deleting.

        """
        assert client.get('/organizations/' + id + '/admins',
                          headers={}).status == '400 BAD REQUEST'

    def organization_post_invitation_no_login(self, client, id):
        assert client.post('/organizations/' + id + '/invitations', headers={},
                           data={
                               'email': 'donaldo@ducko.com',
                               'organization_id': id}).status == '400 BAD ' \
                                                                 'REQUEST'

    def organization_get_invitation_no_login(self, client, id):
        assert client.get('/organizations/' + id + '/invitations',
                          headers={}).status == '400 BAD REQUEST'
