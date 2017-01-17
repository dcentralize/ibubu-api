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
        .. :quickref: Circle; Retrieve a circle.

        Retrieve a circle.

        In order to retrieve a circle, the authenticated user must be a
        partner of the organization that the circle is associated with.

        **Example request**:

        .. sourcecode:: http

            GET /circles/6 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 6,
                'type': 'circle',
                'name': 'Circle\'s name',
                'purpose': 'Circle\'s purpose',
                'strategy': 'Circle\'s strategy',
                'parent_role_id': 1,
                'organization_id': 1
            }

        :param int circle_id: the circle to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the circle's unique id
        :>json string type: the circle's type
        :>json string name: the circle's name
        :>json string purpose: the circle's purpose
        :>json string strategy: the circle's optional strategy
        :>json int parent_role_id: the parent role the circle is related to
        :>json int organization_id: the organization the circle is related to

        :status 200: Circle is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found

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
        .. :quickref: Circle; Update a circle.

        Update a circle.

        In order to update a circle, the authenticated user must be a partner
        of the organization that the circle is associated with.

        **Example request**:

        .. sourcecode:: http

            PUT /circles/6 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'name': 'My Circle\'s new name',
                'purpose': 'My Circle\'s new purpose',
                'strategy': 'My Circle\'s new strategy'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 6,
                'type': 'circle',
                'name': 'My Circle\'s new name',
                'purpose': 'My Circle\'s new purpose',
                'strategy': 'My Circle\'s new strategy',
                'parent_role_id': 1,
                'organization_id': 1
            }

        :param int circle_id: the circle to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the circle's name
        :<json string purpose: the circle's purpose
        :<json string strategy: the circle's strategy

        :resheader Content-Type: data is received as application/json

        :>json int id: the circle's unique id
        :>json string type: the circle's type
        :>json string name: the circle's name
        :>json string purpose: the circle's purpose
        :>json string strategy: the circle's strategy
        :>json int parent_role_id: the parent role the circle is related to
        :>json int organization_id: the organization the circle is related to

        :status 200: Circle is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found

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
        .. :quickref: Circle Roles; Add a role to a circle.

        Add a role to a circle.

        **Example request**:

        .. sourcecode:: http

            POST /circles/1/roles HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'name': 'Role\'s name',
                'purpose': 'Role\'s purpose'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 5,
                'type': 'custom',
                'name': 'My Role\'s name',
                'purpose': 'My Role\'s purpose',
                'parent_role_id': 1,
                'organization_id': 1
            }

        :param int circle_id: the circle the role is added to

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the role's name
        :<json string purpose: the role's purpose

        :resheader Content-Type: data is received as application/json

        :>json int id: the role's unique id
        :>json string type: the role's type
        :>json string name: the role's name
        :>json string purpose: the role's purpose
        :>json int parent_role_id: the parent role the role is related to
        :>json int organization_id: the organization the role is related to

        :status 201: Role is added
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found

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
        .. :quickref: Circle Roles; List roles of a circle.

        List roles of a circle.

        **Example request**:

        .. sourcecode:: http

            GET /circles/1/roles HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 2,
                    'type': 'lead_link',
                    'name': 'Lead Link\'s name',
                    'purpose': 'Lead Link\'s purpose',
                    'parent_role_id': 1,
                    'organization_id': 1
                },
                {
                    'id': 3,
                    'type': 'secretary',
                    'name': 'Secretary\'s name',
                    'purpose': 'Secretary\'s purpose',
                    'parent_role_id': 1,
                    'organization_id': 1
                },
                {
                    'id': 4,
                    'type': 'facilitator',
                    'name': 'Facilitator\'s name',
                    'purpose': 'Facilitator\'s purpose',
                    'parent_role_id': 1,
                    'organization_id': 1
                },
                {
                    'id': 5,
                    'type': 'custom',
                    'name': 'My Role\'s name',
                    'purpose': 'My Role\'s purpose',
                    'parent_role_id': 1,
                    'organization_id': 1
                },
                {
                    'id': 6,
                    'type': 'circle',
                    'name': 'My Circle\'s name',
                    'purpose': 'My Circle\'s purpose',
                    'parent_role_id': 1,
                    'organization_id': 1
                }
            ]

        :param int circle_id: the circle the roles are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the role's unique id
        :>jsonarr string type: the role's type
        :>jsonarr string name: the role's name
        :>jsonarr string purpose: the role's purpose
        :>jsonarr int parent_role_id: the parent role the role is related to
        :>jsonarr int organization_id: the organization the role is related to

        :status 200: Roles are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found

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
    @auth.login_required
    def get(self,
            circle_id):
        """
        .. :quickref: Circle Members; List members of a circle.

        List members of a circle.

        In order to list the members of a circle, the authenticated user must
        be a partner of the organization that the circle is associated with.

        **Example request**:

        .. sourcecode:: http

            GET /circles/1/members HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'type': 'admin',
                    'firstname': 'John',
                    'lastname': 'Doe',
                    'email': 'john@example.org',
                    'is_active': True,
                    'user_id': 1,
                    'organization_id': 1,
                    'invitation_id': null
                }
            ]

        :param int circle_id: the circle the members are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the partner's unique id
        :>jsonarr string type: the partner's type
        :>jsonarr string firstname: the partner's firstname
        :>jsonarr string lastname: the partner's lastname
        :>jsonarr string email: the partner's email address
        :>jsonarr boolean is_active: the partner's status
        :>jsonarr int user_id: the user account the partner is related to
        :>jsonarr int organization_id: the organization the partner is
                                       related to
        :>jsonarr int invitation_id: the invitation the partner is related to

        :status 200: Members are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found

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
    @auth.login_required
    def put(self,
            circle_id,
            partner_id):
        """
        .. :quickref: Circle Members; Assign a partner to a circle.

        Assign a partner to a circle.

        In order to assign a partner to a circle, the authenticated user must
        be an admin of the organization that the circle is associated with.

        **Example request**:

        .. sourcecode:: http

            PUT /circles/1/members/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int circle_id: the circle the partner is assigned to
        :param int partner_id: the partner who is assigned to the circle

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Partner is assigned to circle
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found
        :status 404: Partner is not found
        :status 409: Circle is not associated with partner's organization

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        if circle.super.organization_id != partner.organization_id:
            abort(409, 'Cannot assign a partner to a circle that is not '
                       'associated with the partner\'s organization.')

        circle.super.members.append(partner)
        db.session.commit()

        return None, 204

    @auth.login_required
    def delete(self,
               circle_id,
               partner_id):
        """
        .. :quickref: Circle Members; Unassign a partner from a circle.

        Unassign a partner from a circle.

        In order to unassign a partner from a circle, the authenticated user
        must be an admin of the organization that the circle is associated
        with.

        **Example request**:

        .. sourcecode:: http

            DELETE /circles/1/members/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int circle_id: the circle the partner is unassigned from
        :param int partner_id: the partner who is unassigned from the circle

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Partner is unassigned from circle
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Circle is not found
        :status 404: Partner is not found

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
