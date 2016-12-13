"""
Define the classes for the circle API.

"""
from flask import abort
from flask_restful import reqparse, Resource
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
    def get(self,
            circle_id):
        """
        Retrieve a circle.

        In order to retrieve a circle, the authenticated user must be a member
        or an admin of the organization that the circle is associated with.

        Request:
            GET /circles/{circle_id}

        Response:
            200 OK - If circle is retrieved
                {
                    'id': 1,
                    'type': 'circle',
                    'name': 'Circle\'s name',
                    'purpose': 'Circle\'s purpose',
                    'strategy': 'Circle\'s strategy',
                    'parent_circle_id': null|1,
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found

        """

        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        data = {}
        data.update(circle.super.serialize)
        data.update(circle.serialize)

        return data, 200

    @auth.login_required
    def put(self,
            circle_id):
        """
        Update a circle.

        In order to edit a circle, the authenticated user must be an admin
        of the organization that the circle is associated with.

        Request:
            PUT /circles/{circle_id}

            Parameters:
                name (string): The name of the circle
                purpose (string): The purpose of the circle
                strategy (string): The strategy of the circle

        Response:
            200 OK - If circle is updated
                {
                    'id': 1,
                    'type': 'circle',
                    'name': 'Circle\'s name',
                    'purpose': 'Circle\'s purpose',
                    'strategy': 'Circle\'s strategy',
                    'parent_circle_id': null|1,
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose', required=True)
        parser.add_argument('strategy')
        args = parser.parse_args()

        circle.super.name = args['name']
        circle.super.purpose = args['purpose']
        circle.strategy = args['strategy']
        db.session.commit()

        data = {}
        data.update(circle.super.serialize)
        data.update(circle.serialize)

        return data, 200


class CircleRoles(Resource):
    """
    Define the endpoints for the roles edge of the circle node.

    """
    @auth.login_required
    def post(self,
             circle_id):
        """
        Add a role to a circle.

        Request:
            POST /circles/{circle_id}/roles

            Parameters:
                name (string): The name of the role
                purpose (string): The purpose of the role

        Response:
            204 No Content - If role is added to circle
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose', required=True)
        args = parser.parse_args()

        role = RoleModel(RoleType.custom,
                         args['name'],
                         args['purpose'],
                         circle.super.id,
                         circle.super.organization_id)
        circle.roles.append(role)
        db.session.commit()

        return role.serialize, 201

    @auth.login_required
    def get(self,
            circle_id):
        """
        List roles of a circle.

        Request:
            GET /circles/{circle_id}/roles

        Response:
            200 OK - If roles of circle are listed
                [
                    {
                        'id': 1,
                        'type': 'circle|lead_link|secretary|custom',
                        'name': 'Role\'s name',
                        'purpose': 'Role\'s purpose',
                        'parent_circle_id': 1,
                        'organization_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        data = [i.serialize for i in circle.roles]

        return data, 200


class CircleMembers(Resource):
    """
    Define the endpoints for the members edge of the circle node.

    """
    def get(self,
            circle_id):
        """
        List members of a circle.

        In order to list the members of a circle, the authenticated user must
        be a member or an admin of the organization that the circle is
        associated with.

        Request:
            GET /circles/{circle_id}/members

        Response:
            200 OK - If members of circle are listed
                [
                    {
                        'id': 1,
                        'type': 'member|admin',
                        'firstname': 'John',
                        'lastname': 'Doe',
                        'email': 'john@example.org',
                        'is_active': True|False,
                        'user_id': 1,
                        'organization_id': 1,
                        'invitation_id': null|1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        data = [i.serialize for i in circle.super.members]

        return data, 200


class CircleMembersAssociation(Resource):
    """
    Define the endpoints for the members association edge of the circle node.

    """
    def put(self,
            circle_id,
            partner_id):
        """
        Assign a partner to a circle.

        In order to assign a partner to a circle, the authenticated user must
        be an admin of the organization that the circle is associated with.

        Request:
            PUT /circles/{circle_id}/members/{partner_id}

        Response:
            204 No Content - If partner is assigned to circle
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found
            404 Not Found - If partner is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        circle.super.members.append(partner)
        db.session.commit()

        return None, 204

    def delete(self,
               circle_id,
               partner_id):
        """
        Unassign a partner from a circle.

        In order to unassign a partner from a circle, the authenticated user
        must be an admin of the organization that the circle is associated
        with.

        Request:
            DELETE /circles/{circle_id}/members/{partner_id}

        Response:
            204 No Content - If partner is unassigned from circle
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If circle is not found
            404 Not Found - If partner is not found

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        circle.super.members.remove(partner)
        db.session.commit()

        return None, 204
