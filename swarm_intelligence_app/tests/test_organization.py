# """
# Test user api-functionality.
# """
#
# from swarm_intelligence_app.tests import test_helper
#
#
# class TestOrganization:
#     """
#     Class for testing user api-functionality.
#
#     """
#     helper = test_helper.TestHelper
#     token = 'mock_user_001'
#
#     def set_up_test(self, client):
#         self.helper.set_up(test_helper, client)
#
#     def test_me_post(self, client):
#         """
#         Test if the me-page returns a valid http status-code when posting.
#         """
#         assert client.post('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#         print('Passed test for creating a new user.')
#
#     def test_me_organizations_post(self, client):
#         """
#         Test if the me-organizations-page returns a valid http status-code.
#         when posting.
#         """
#         assert client.post('/me/organizations', headers={
#             'Authorization': 'Token ' + self.token},
#                            data={'name': 'Dagoberts ' + 'Empire'}).status == \
#                '200 OK'
#         print('Passed test for creating a new organization.')
#
#     def test_get_organization_id(self, client):
#         """
#         Helper Method for getting an organization ID for further tests.
#         """
#
#         data = client.get('/me/organizations', headers={
#             'Authorization': 'Token ' + self.token}).json['data'][0]['id']
#         organization_id = str(data)
#         return organization_id
#
#     def test_get_organization(self, client):
#         """
#         Test if get request to API gets executed
#         """
#         assert client.get('/organizations/' + self.test_get_organization_id(
#             client), headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#
#         print('Passed test for getting an Organization.')
#
#     def test_put_organization(self, client):
#         """
#         Test if get request to API gets executed
#         """
#         assert client.put('/organizations/' + self.test_get_organization_id(
#             client), headers={
#             'Authorization': 'Token ' + self.token},
#                           data={'is_deleted': 'False', 'name': 'Tolli Empire',
#                                 'id': '1'}).status == '200 OK'
#
#         print('Passed test for putting an Organization.')
#
#     def test_delete_organization(self, client):
#         """
#         Test if the delete request gets executed
#         """
#         assert client.delete('/organizations/' + self.test_get_organization_id(
#             client), headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#
