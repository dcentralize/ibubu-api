"""
Define the classes for the domain API.

"""
from flask_restful import Resource
# from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
# from swarm_intelligence_app.models import db
# from swarm_intelligence_app.models.domain import Domain as \
#     DomainModel


class Policy(Resource):
    """
    Define the endpoints for the roles edge of the domain node.

    """

    @auth.login_required
    def get(self, domain_id):
        """
        Retrieve a domain.

        Args:
            domain_id: The id of the domain to display.

        Body:

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': {
                        'id': '2',
                        'name': 'Finances',
                        'role_id': '1'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The domain with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        # ToDo

    @auth.login_required
    def put(self, domain_id):
        """
        Edit a domain.

        Args:
            domain_id: The id of the domain which to edit.

        Body:
            name: The name of the domain.

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': {
                        'id': '2',
                        'name': 'Finances',
                        'role_id': '1'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The domain with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        # ToDO

    @auth.login_required
    def delete(self, domain_id):
        """
        Delete a policy.

        Args:
            domain_id: The id of the domain which to delete.

        Body:

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': { }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The domain with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        # ToDo
