"""
Define the classes for the policy API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.policy import Policy as \
     PolicyModel


class Policy(Resource):
    """
    Define the endpoints for the policy node.

    """

    @auth.login_required
    def get(self, policy_id):
        """
        Retrieve a accountability.

        Args:
            policy_id: The id of the policy to display.

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
                        'title': 'Finances',
                        'description': 'Keys for the safe.',
                        'domain_id': '1'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The policy with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            raise errors.EntityNotFoundError('policy', policy_id)

        return {
                   'success': True,
                   'data': policy.serialize
               }, 200

    @auth.login_required
    def put(self, policy_id):
        """
        Edit a policy.

        Args:
            policy_id: The id of the policy which to edit.

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
                        'title': 'Finances',
                        'description': 'Keys for the safe.',
                        'domain_id': '1'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The policy with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            raise errors.EntityNotFoundError('policy', policy_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        args = parser.parse_args()

        policy.title = args['title']
        policy.description = args['descrition']
        db.session.commit()

        return {
                   'success': True,
                   'data': policy.serialize
               }, 200

    @auth.login_required
    def delete(self, policy_id):
        """
        Delete a policy.

        Args:
            policy_id: The id of the policy which to delete.

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
                            'message': 'The policy with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            raise errors.EntityNotFoundError('policy', policy_id)

        db.session.delete(policy)
        db.session.commit()

        return {
                   'success': True
               }, 200
