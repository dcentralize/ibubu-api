"""
Define the classes for the circle API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.role import Role as RoleModel
from swarm_intelligence_app.models.role import RoleType


class Circle(Resource):
    """
    Define the endpoints for the circle node.

    """

    @auth.login_required
    def get(self, circle_id):
        """
        Retrieve a circle.

        In order to retrieve a circle, the authenticated user must be a member
        or an admin of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to retrieve

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        return {
                   'success': True,
                   'data': circle.serialize
               }, 200

    @auth.login_required
    def put(self,
            circle_id):
        """
        Edit a circle.

        In order to edit a circle, the authenticated user must be an admin
        of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to edit

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose')
        parser.add_argument('strategy')
        args = parser.parse_args()

        circle.name = args['name']
        circle.purpose = args['purpose']
        circle.strategy = args['strategy']
        db.session.commit()

        return {
                   'success': True,
                   'data': circle.serialize
               }, 200

    @auth.login_required
    def delete(self,
               circle_id):
        """
        Delete a circle.

        In order to delete a circle, the authenticated user must be an admin
        of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to delete

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        db.session.delete(circle)
        db.session.commit()

        return {
            'success': True
        }


class CircleSubcircles(Resource):
    """
    Define the endpoints for the subcircles edge of the circle node.

    """

    @auth.login_required
    def get(self,
            circle_id):
        """
        List subcircles of a circle.

        In order to list the subcircles of a circle, the authenticated user
        must be a member or an admin of the organization that the circle is
        associated with.

        Args:
            circle_id: The id of the circle for which to list the subcircles

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        data = []
        for i in circle.roles:
            if i.type == RoleType.CIRCLE:

                data.append({
                    'id_role': i.id,
                    'name': i.name,
                    'type': i.type.value,
                    'role_circle_id': i.circle_id,
                    'parent_circle_id': i.parent_circle_id,
                    'purpose': i.purpose,
                    'circle_id': i.subcircle[0].id,
                    'strategy': i.circle.strategy,
                    'role_id': i.subcircle[0].role_id,
                    'organization_id': i.circle.organization_id
                })

        return {
                   'success': True,
                   'data': data
               }, 200


class CircleRole(Resource):
    """
    Define the endpoints for the role edge of the circle node.

    """

    @auth.login_required
    def put(self, circle_id):
        """
        Change the circle back to the role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()


class CircleRoles(Resource):
    """
    Define the endpoints for the roles edge of the circle node.

    """

    @auth.login_required
    def post(self, circle_id):
        """
        Add a role to a circle.

        Args:
            circle_id: The id of the circle for which to add the new role

        Body:
            name: The name of the role
            purpose: A Description of the purpose role

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': {
                        'email': 'donald@gmail.de',
                        'firstname': 'Donald',
                        'google_id': 'mock_user_001',
                        'id': '1',
                        'is_deleted': false,
                        'lastname': 'Duck'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The user with id 1 does not exist'
                          }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose', required=True)
        args = parser.parse_args()

        role = RoleModel(args['name'], args['purpose'], None,
                         circle_id, RoleType.CUSTOM)
        db.session.add(role)
        circle.roles.append(role)
        db.session.commit()
        return {
                   'success': True,
                   'data': role.serialize
               }, 200

    @auth.login_required
    def get(self, circle_id):
        """
        List all roles of a circle.

        Params:
            circle_id: The id of the circle for which to add the new role
        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        data = []
        for i in circle.roles:
            if i.type != RoleType.CIRCLE:
                data.append(i.serialize)
        return {
                   'success': True,
                   'data': data
               }, 200


class CircleMembers(Resource):
    """
    Define the endpoints for the members edge of the circle node.

    """

    @auth.login_required
    def get(self, circle_id):
        """
        List members of a circle.

        In order to list the members of a circle, the authenticated user must
        be a member or an admin of the organization that the circle is
        associated with.

        Args:
            circle_id: The id of the circle for which to list the members

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        data = [i.serialize for i in circle.partners]
        return {
            'success': True,
            'data': data
        }

    @auth.login_required
    def put(self,
            circle_id,
            partner_id):
        """
        Assign a partner to a circle.

        In order to assign a partner to a circle, the authenticated user must
        be an admin of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to assign the partner to
            partner_id: The id of the partner to assign

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)

        circle.partners.append(partner)
        db.session.commit()

        return {
                   'success': True
               }, 200

    @auth.login_required
    def delete(self,
               circle_id,
               partner_id):
        """
        Unassign a partner from a circle.

        In order to unassign a partner from a circle, the authenticated user
        must be an admin of the organization that the circle is associated
        with.

        Args:
            circle_id: The id of the circle to unassign the partner from
            partner_id: The id of the partner to unassign

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)

        circle.partners.remove(partner)
        db.session.commit()

        return {
                   'success': True
               }, 200
