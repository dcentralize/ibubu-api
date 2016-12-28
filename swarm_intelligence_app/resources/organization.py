"""
Define the classes for the organization API.

"""
from flask import abort
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.partner import \
    Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.role import Role as RoleModel


class Organization(Resource):
    """
    Define the endpoints for the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        Retrieve an organization.

        In order to retrieve an organization, the authenticated user must be a
        member or an admin of the organization.

        Request:
            GET /organizations/{organization_id}

        Response:
            200 OK - If organization is retrieved
                {
                    'id': 1,
                    'name': 'My Company'
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        return organization.serialize, 200

    @auth.login_required
    def put(self,
            organization_id):
        """
        Update an organization.

        In order to edit an organization, the authenticated user must be an
        admin of the organization.

        Request:
            PUT /organizations/{organization_id}

            Parameters:
                name (string): The name of the organization

        Response:
            200 OK - If organization is updated
                {
                    'id': 1,
                    'name': 'My Company'
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        organization.name = args['name']
        db.session.commit()

        return organization.serialize, 200

    @auth.login_required
    def delete(self,
               organization_id):
        """
        Delete an organization.

        This endpoint sets the organization's state to 'deleted', so that it
        cannot be accessed by its members or admins in any way. In order to
        delete an organization, the authenticated user must be an admin of the
        organization.

        Request:
            DELETE /organizations/{organization_id}

        Response:
            204 No Content - If organization is deleted
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        db.session.delete(organization)
        db.session.commit()

        return None, 204


class OrganizationAnchorCircle(Resource):
    """
    Define the endpoints for the anchor circle edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        Retrieve the anchor circle of an organization.

        This endpoint retrieves the anchor circle of an organization. Each
        organization has exactly one circle as its anchor circle. In order to
        retrieve the anchor circle of an organization, the authenticated user
        must be a member or an admin of the organization.

        Request:
            GET /organizations/{organization_id}/anchor_circle

        Response:
            200 OK - If organization's anchor circle is retrieved
                {
                    'id': 1,
                    'type': 'circle',
                    'name': 'My Company',
                    'pupose': 'My Company\'s purpose',
                    'strategy': 'My Company\'s strategy',
                    'parent_circle_id': null,
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        null_value = None
        role, circle = db.session.query(
            RoleModel, CircleModel).join(
            CircleModel, RoleModel.id == CircleModel.id).filter(
            RoleModel.organization_id == organization.id).filter(
            RoleModel.parent_circle_id == null_value).first()

        if role is None or circle is None:
            abort(404)

        data = {}
        data.update(role.serialize)
        data.update(circle.serialize)

        return data, 200


class OrganizationMembers(Resource):
    """
    Define the endpoints for the members edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        List members of an organization.

        This endpoint lists all partners with access through membership or with
        admin access to the organization, whether their state is 'active' or
        not. In order to list the members of an organization, the
        authenticated user must be a member or an admin of the organization.

        Request:
            GET /organizations/{organization_id}/members

        Response:
            200 OK - If members of organization are listed
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
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        data = [i.serialize for i in organization.partners]

        return data, 200


class OrganizationAdmins(Resource):
    """
    Define the endpoints for the admins edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        List admins of an organization.

        This endpoint lists all partners of an organization with admin access
        to the organization, whether their state is 'active' or not. In order
        to list the admins of an organization, the authenticated user must be
        a member or an admin of the organization.

        Request:
            GET /organizations/{organization_id}/admins

        Response:
            200 OK - If admins of organization are listed
                [
                    {
                        'id': 1,
                        'type': 'admin',
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
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        admins = PartnerModel.query.filter_by(organization=organization,
                                              type=PartnerType.admin).all()

        data = [i.serialize for i in admins]

        return data, 200


class OrganizationInvitations(Resource):
    """
    Define the endpoints for the invitations edge of the organization node.

    """
    @auth.login_required
    def post(self,
             organization_id):
        """
        Invite a user to an organization.

        This endpoint will send an invitation to a given email address. The
        newly-created invitation will be in the 'pending' state until the user
        accepts the invitation. At this point the invitation will transition
        to the 'accepted' state and the user will be added as a new partner to
        the organization. In order to invite a user to an organization, the
        authenticated user must be an admin of the organization.

        Request:
            POST /organizations/{organization_id}/invitations

            Parameters:
                email (string): The email address the invitation is sent to

        Response:
            201 Created - If invitation is created
                {
                    'id': 1,
                    'code': '12345678-1234-1234-1234-123456789012',
                    'email': 'john@example.org',
                    'status': 'pending|accepted|cancelled',
                    'organization_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        invitation = InvitationModel(
            args['email'],
            organization.id
        )
        organization.invitations.append(invitation)

        db.session.add(invitation)
        db.session.commit()

        return invitation.serialize, 201

    @auth.login_required
    def get(self,
            organization_id):
        """
        List invitations to an organization.

        This endpoint lists all 'pending', 'accepted' and 'cancelled'
        invitations to an organization. In order to list invitations to an
        organization, the authenticated user must be a member or an admin of
        the organization.

        Request:
            GET /organizations/{organization_id}/invitations

        Response:
            200 OK - If invitations to organization are listed
                [
                    {
                        'id': 1,
                        'code': '12345678-1234-1234-1234-123456789012',
                        'email': 'john@example.org',
                        'status': 'pending|accepted|cancelled',
                        'organization_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        invitations = InvitationModel.query.filter_by(
            organization_id=organization.id)

        data = [i.serialize for i in invitations]

        return data, 200
