"""
Define the classes for the accountability API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.accountability import Accountability as \
    AccountabilityModel


class Accountability(Resource):
    """
    Define the endpoints for the accountability node.

    """

    @auth.login_required
    def get(self, accountability_id):
        """
        Retrieve a accountability.

        Args:
            accountability_id: The id of the accountability to display.

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
                            'message': 'The accountability with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            raise errors.EntityNotFoundError('accountability',
                                             accountability_id)

        return {
                   'success': True,
                   'data': accountability.serialize
               }, 200

    @auth.login_required
    def put(self, accountability_id):
        """
        Edit a accountability.

        Args:
            accountability_id: The id of the accountability which to edit.

        Body:
            name: The name of the accountability.

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
                            'message': 'The accountability with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            raise errors.EntityNotFoundError('accountability',
                                             accountability_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        accountability.name = args['name']
        db.session.commit()

        return {
                   'success': True,
                   'data': accountability.serialize
               }, 200

    @auth.login_required
    def delete(self, accountability_id):
        """
        Delete a accountability.

        Args:
            accountability_id: The id of the accountability which to delete.

        Body:

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The accountability with id 1 does not
                            exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            raise errors.EntityNotFoundError('accountability',
                                             accountability_id)

        db.session.delete(accountability)
        db.session.commit()

        return {
                   'success': True
               }, 200
