"""
Define the classes for the role API.

"""
from flask import abort
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.accountability import Accountability as \
    AccountabilityModel
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.domain import Domain as DomainModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.role import Role as RoleModel
from swarm_intelligence_app.models.role import RoleType


class Role(Resource):
    """
    Define the endpoints for the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        Retrieve a role.

        Request:
            GET /roles/{role_id}

        Response:
            200 OK - If role is retrieved
                {
                    'id': 1,
                    'type': 'circle|lead_link|secretary|facilitator|custom',
                    'name': 'Role\'s name,
                    'purpose': 'Role\'s purpose,
                    'parent_circle_id': null|1,
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        return role.serialize, 200

    @auth.login_required
    def put(self, role_id):
        """
        Update a role.

        Request:
            PUT /roles/{role_id}

            Parameters:
                name (string): The name of the role
                purpose (string): The purpose of the role

        Response:
            200 OK - If role is updated
                {
                    'id': 1,
                    'type': 'circle|lead_link|secretary|facilitator|custom',
                    'name': 'Role\'s name,
                    'purpose': 'Role\'s purpose,
                    'parent_circle_id': null|1,
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose', required=True)
        args = parser.parse_args()

        role.name = args['name']
        role.purpose = args['purpose']
        db.session.commit()

        return role.serialize, 200

    @auth.login_required
    def delete(self, role_id):
        """
        Delete a role.

        In order to delete a partner, the authenticated user must be an admin
        of the organization that the partner is associated with.

        Request:
            DELETE /roles/{role_id}

        Response:
            204 No Content - If role is deleted
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not found - If role is not found
            409 Conflict - If type of role is other than custom
            409 Conflict - If role is an anchor circle of an organization

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type != RoleType.custom:
            abort(409, 'Cannot delete role of type other than custom circle.')

        if role.parent_circle_id is None:
            abort(409, 'The anchor circle of an organization cannot be '
                       'deleted.')

        db.session.delete(role)
        db.session.commit()

        return None, 204


class RoleMembers(Resource):
    """
    Define the endpoints for the members edge of the role node.

    """
    def get(self,
            role_id):
        """
        List members of a role.

        Request:
            GET /roles/{role_id}/members

        Response:
            200 OK - If members of role are listed
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
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.members]

        return data, 200


class RoleMembersAssociation(Resource):
    """
    Define the endpoints for the members association edge of the role node.

    """
    def put(self,
            role_id,
            partner_id):
        """
        Assign a partner to a role.

        Request:
            PUT /roles/{role_id}/members/{partner_id}

        Response:
            204 No Content - If partner is assigned to role
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found
            404 Not Found - If partner is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        role.members.append(partner)
        db.session.commit()

        return None, 204

    def delete(self,
               role_id,
               partner_id):
        """
        Unassign a partner from a role.

        Request:
            DELETE /roles/{role_id}/members/{partner_id}

        Response:
            204 No Content - If partner is unassigned from role
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found
            404 Not Found - If partner is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        role.members.remove(partner)
        db.session.commit()

        return None, 204


class RoleDomains(Resource):
    """
    Define the endpoints for the domain edge of the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        List all domains of a role.

        Request:
            GET /roles/{role_id}/domains

        Response:
            200 OK - If domains of role are listed
                [
                    {
                        'id': 1,
                        'title': 'Role\'s name',
                        'role_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.domains]

        return data, 200

    @auth.login_required
    def post(self, role_id):
        """
        Add a domain to a role.

        Request:
            POST /roles/role_id/domains

            Parameters:
                title (string): The title of the domain

        Response:
            201 Created - If domain is added
                {
                    'id': 1,
                    'title': 'Role\'s name',
                    'role_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Conflict - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        domain = DomainModel(args['title'], role.id)

        role.domains.append(domain)
        db.session.commit()

        return domain.serialize, 200


class RoleAccountabilities(Resource):
    """
    Define the endpoints for the accountability edge of the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        List all accountabilities of a role.

        Request:
            GET /roles/{role_id}/accountabilities

        Response:
            200 OK - If accountabilities of role are listed
                [
                    {
                        'id': 1,
                        'title': 'Accountabilities\' title',
                        'role_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.accountabilities]

        return data, 200

    @auth.login_required
    def post(self, role_id):
        """
        Add a accountability to a role.

        Request:
            POST /roles/{role_id}/accountabilities

            Parameters:
                title (string): The title of the accountability

        Response:
            201 Created - If accountability is added
                {
                    'id': 1,
                    'title': 'Accountabilities\' title',
                    'role_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        accountability = AccountabilityModel(args['title'], role.id)

        role.accountabilities.append(accountability)
        db.session.commit()

        return accountability.serialize, 201


class RoleCircle(Resource):
    """
    Define the endpoints for the circle edge of the role node.

    """
    @auth.login_required
    def put(self,
            role_id):
        """
        Add circle properties to a role.

        Request:
            PUT /roles/{role_id}/circle

        Response:
            204 No Content - If circle properties are added to role
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found
            409 Conflict - If type of role is other than custom

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type == RoleType.circle:
            pass
        elif role.type == RoleType.custom:
            try:
                role.type = RoleType.circle

                circle = CircleModel(role.id, None)
                db.session.add(circle)
                db.session.flush()

                lead_link = RoleModel(RoleType.lead_link, 'Lead Link',
                    'Lead Link\'s Purpose', role.id, role.organization_id)
                db.session.add(lead_link)

                secretary = RoleModel(RoleType.secretary, 'Secretary',
                    'Secretary\'s Purpose', role.id, role.organization_id)
                db.session.add(secretary)

                facilitator = RoleModel(RoleType.facilitator, 'Facilitator',
                    'Facilitator\'s Purpose', role.id, role.organization_id)
                db.session.add(facilitator)

                db.session.commit()
            except:
                db.session.rollback()
                abort(409, 'Cannot add circle properties to this role.')
        else:
            abort(409, 'Cannot add circle properties to a role that is not a '
                       'custom role.')

        return None, 204


    @auth.login_required
    def delete(self,
               role_id):
        """
        Remove circle properties from a role.

        Request:
            DELETE /roles/{role_id}/circle

        Response:
            204 No Content - If circle properties are removed from role
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If role is not found
            409 Conflict - If type of role is other than custom
            409 Conflict - If role is an anchor circle of an organization

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type != RoleType.circle:
            abort(409, 'Cannot remove circle properties from a role that is '
                       'not a circle.')

        if role.parent_circle is None:
            abort(409, 'Cannot remove circle properties from a role that is '
                       'an anchor circle.')

        try:
            role.type = RoleType.custom

            db.session.delete(role.derived_circle)
            db.session.commit()
        except:
            db.session.rollback()
            abort(409, 'Cannot remove circle properties from this role.')

        return None, 204
