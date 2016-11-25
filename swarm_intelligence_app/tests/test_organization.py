"""
Test user api-functionality.
"""


class TestOrganization:
    """
    Class for testing user api-functionality.

    """
    token = 'mock_user_001'

    print('=====Start Testing Organization=====')

    # def test_me_post(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when posting.
    #     """
    #     assert client.post('/me', headers={
    #         'Authorization': 'Token ' + self.token}).status == '200 OK'
    #     print('Passed test for creating a new user.')

    # def test_me_post(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when posting.
    #     """
    #     assert client.post('/me', headers={
    #         'Authorization': 'Token ' + self.token}).status == '200 OK'
    #     print('Passed test for creating a new user.')
    #
    #
    # def test_me_organizations_post(self, client):
    #     """
    #     Test if the me-organizations-page returns a   valid http status-code.
    #     when posting.
    #     """
    #     self.test_me_post(client)
    #     assert client.post('/me/organizations', headers={
    #         'Authorization': 'Token ' + self.token},
    #                        data={'name': 'Dagoberts ' + 'Empire'}).status == \
    #            '200 OK'
    #     print('Passed test for creating a new organization.')


print('=====End Testing Organization=====')
