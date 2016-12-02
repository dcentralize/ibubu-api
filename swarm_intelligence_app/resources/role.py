"""
Define the classes for the role API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.role import Role as RoleModel


class Role(Resource):
    """
    Define the endpoints for the role node.

    """

    @auth.login_required
    def get(self, role_id):
        """
        Retrieve role details.

        Args:
            role_id: The id of the role to retrieve details.

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
                        'circle_id': '1',
                        'id': '5',
                        'name': 'Manager',
                        'parent_circle_id': null,
                        'purpose': 'Manager of the soccer club.',
                        'type': 'custom'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The role with id 1 does not exist'
                        }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        role = RoleModel.query.get(role_id)

        if role is None:
            raise errors.EntityNotFoundError('role', role_id)

        return {
                   'success': True,
                   'data': role.serialize
               }, 200

    @auth.login_required
    def put(self, role_id):
        """
        Edit role details.

        Args:
            role_id: The id of the role to retrieve details.

        Body:
            name: The name of the role.
            purpose: The purpose of the role.

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': {
                        'circle_id': '1',
                        'id': '5',
                        'name': 'Manager',
                        'parent_circle_id': null,
                        'purpose': 'Manager of the soccer club.',
                        'type': 'custom'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The role with id 1 does not exist'
                        }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        role = RoleModel.query.get(role_id)
        if role is None:
            raise errors.EntityNotFoundError('role', role_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose')
        args = parser.parse_args()

        role.name = args['name']
        role.purpose = args['purpose']
        db.session.commit()
        return {
                   'success': True,
                   'data': role.serialize
               }, 200

    @auth.login_required
    def delete(self, role_id):
        """
        Delete a role.

        Args:
            role_id: The id of the role to retrieve details.

        Body:

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': null,
            }
            {
                'success': False,
                'errors': {
                        'circle_id': '1',
                        'id': '5',
                        'name': 'Manager',
                        'parent_circle_id': null,
                        'purpose': 'Manager of the soccer club.',
                        'type': 'custom'
                        }
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        role = RoleModel.query.get(role_id)

        if role is None:
            raise errors.EntityNotFoundError('role', role_id)

        db.session.delete(role)
        db.session.commit()

        role = RoleModel.query.get(role_id)
        if role is None:
            return {
                       'success': True,
                       'data': role
                   }, 200
        else:
            return {
                       'success': False,
                       'data': role.serialize
                   }, 200


class RoleMembers(Resource):
    """
    Define the endpoints for the members edge of the role node.

    """
    def get(self, role_id):
        """
        List members of a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()

    def put(self, role_id, partner_id):
        """
        Assign a partner to a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()

    def delete(self, role_id, partner_id):
        """
        Unassign a partner from a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()


class RoleCircle(Resource):
    """
    Define the endpoints for the circle edge of the role node.

    """
    def put(self, role_id):
        """
        Update the role to a circle.

        """
        # ToDO
        raise errors.MethodNotImplementedError()
