"""
Define the classes for the domain API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.domain import Domain as \
     DomainModel
from swarm_intelligence_app.models.policy import Policy as PolicyModel


class Domain(Resource):
    """
    Define the endpoints for the domain node.

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
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            raise errors.EntityNotFoundError('domain', domain_id)

        return {
                   'success': True,
                   'data': domain.serialize
               }, 200

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
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            raise errors.EntityNotFoundError('domain', domain_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        domain.name = args['name']
        db.session.commit()

        return {
                   'success': True,
                   'data': domain.serialize
               }, 200

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
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            raise errors.EntityNotFoundError('domain', domain_id)

        db.session.delete(domain)
        db.session.commit()

        return {
                   'success': True
               }, 200


class DomainPolicies(Resource):
    """
    Define the endpoints for the policy edge of the domain node.

    """

    @auth.login_required
    def get(self, domain_id):
        """
        List of all policies of a domain.

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
                            {
                            'id': '2',
                            'title': 'Finances',
                            'description': 'Keys for the safe.',
                            'domain_id': '1'
                            },
                            {
                            'id': '3',
                            'title': 'Permissions',
                            'description': 'Description of persmissions.',
                            'domain_id': '1'
                            }
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
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            raise errors.EntityNotFoundError('domain', domain_id)

        data = [i.serialize for i in domain.policies]
        return {
                   'success': True,
                   'data': data
               }, 200

    @auth.login_required
    def post(self, domain_id):
        """
        Create a new policy for the domain.

        Args:
            domain_id: The id of the domain which to edit.

        Body:
            title: The title of the policy.
            description: The description of the policy.

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
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            raise errors.EntityNotFoundError('domain', domain_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        args = parser.parse_args()

        policy = PolicyModel(args['title'], args['description'], domain.id)
        domain.policies.append(policy)
        db.session.commit()

        return {
                   'success': True,
                   'data': policy.serialize
               }, 200
