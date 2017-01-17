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
        .. :quickref: Organization; Retrieve an Organization.

        Retrieve an organization.

        In order to retrieve an organization, the authenticated user must be a
        member or an admin of the organization.

        **Example request**:

        .. sourcecode:: http

            GET /organizations/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'name': 'My Organization'
            }

        :param int organization_id: the organization to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the organization's unique id
        :>json string name: the organization's name

        :status 200: Organization is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        return organization.serialize, 200

    @auth.login_required
    def put(self,
            organization_id):
        """
        .. :quickref: Organization; Update an organization.

        Update an organization.

        In order to update an organization, the authenticated user must be an
        admin of the organization.

        **Example request**:

        .. sourcecode:: http

            PUT /organizations/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'name': 'My Organization'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'name': 'My Organization'
            }

        :param int organization_id: the organization to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the organization's name

        :resheader Content-Type: data is received as application/json

        :>json int id: the organization's unique id
        :>json string name: the organization's name

        :status 200: Organization is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization; Delete an organization.

        Delete an organization.

        In order to delete an organization, the authenticated user must be an
        admin of the organization.

        **Example request**:

        .. sourcecode:: http

            DELETE /organizations/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int organization_id: the organization to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Organization is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization Anchor Circle; Retrieve the anchor circle.

        Retrieve the anchor circle of an organization.

        This endpoint retrieves the anchor circle of an organization. Each
        organization has exactly one circle as its anchor circle. In order to
        retrieve the anchor circle of an organization, the authenticated user
        must be a member or an admin of the organization.

        **Example request**:

        .. sourcecode:: http

            GET /organizations/1/anchor_circle HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'type': 'circle',
                'name': 'My Organization',
                'pupose': 'My Organization\'s purpose',
                'strategy': 'My Organizations\'s strategy',
                'parent_circle_id': null,
                'organization_id': 1
            }

        :param int organization_id: the organization to retrieve the anchor
                                    circle of

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the anchor circle's unique id
        :>json string type: the anchor circle's type
        :>json string name: the anchor circle's name
        :>json string purpose: the anchor circle's purpose
        :>json string strategy: the anchor circle's strategy
        :>json int parent_role_id: the role the anchor circle is a child of
        :>json int organization_id: the organization the anchor circle is
                                    related to

        :status 200: Anchor circle is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization Members; List members of an organization.

        List partners of an organization.

        This endpoint lists all members of an organization, whether their
        status is 'active' or not. In order to list the members of an
        organization, the authenticated user must be a members of the
        organization.

        **Example request**:

        .. sourcecode:: http

            GET /organizations/1/members HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'type': 'member',
                    'firstname': 'John',
                    'lastname': 'Doe',
                    'email': 'john@example.org',
                    'is_active': True,
                    'user_id': 1,
                    'organization_id': 1,
                    'invitation_id': null
                }
            ]

        :param int organization_id: the organization the members are listed
                                    for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the member's unique id
        :>jsonarr string type: the member's type
        :>jsonarr string firstname: the member's firstname
        :>jsonarr string lastname: the member's lastname
        :>jsonarr string email: the member's email address
        :>jsonarr boolean is_active: the member's status
        :>jsonarr int user_id: the user account the member is related to
        :>jsonarr int organization_id: the organization the member is
                                       related to
        :>jsonarr int invitation_id: the invitation the member is related to

        :status 200: Members are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization Admins; List admins of an organization.

        List partners with admin access of an organization.

        This endpoint lists all partners with admin access of an organization,
        whether their status is 'active' or not. In order to list the partners
        with admin access of an organization, the authenticated user must be a
        partner of the organization.

        **Example request**:

        .. sourcecode:: http

            GET /organizations/1/admins HTTP/1.1
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

        :param int organization_id: the organization the partners with admin
                                    access are listed for

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

        :status 200: Partners with admin access are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization Invitations; Invite a user to an
                      organization.

        Invite a user to an organization.

        This endpoint will send an invitation to a given email address. The
        newly-created invitation will be in the 'pending' state until the user
        accepts the invitation. At this point the invitation will transition
        to the 'accepted' state and the user will be added as a new partner to
        the organization. In order to invite a user to an organization, the
        authenticated user must be an admin of the organization.

        **Example request**:

        .. sourcecode:: http

            POST /organizations/1/invitations HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'email': 'john@example.org'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 1,
                'code': '12345678-1234-1234-1234-123456789012',
                'email': 'john@example.org',
                'status': 'pending',
                'organization_id': 1
            }

        :param int organization_id: the organization the invitation is created
                                    for

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string email: the email address the invitation is sent to

        :resheader Content-Type: data is received as application/json

        :>json int id: the invitation's unique id
        :>json string code: the invitation's unique code
        :>json string email: the email address the invitation is sent to
        :>json string status: the invitation's status
        :>json int organization_id: the organization the invitation is related
                                    to

        :status 201: Invitation is created
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

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
        .. :quickref: Organization Invitations; List invitations to an
                      organization.

        List invitations to an organization.

        This endpoint lists all 'pending', 'accepted' and 'cancelled'
        invitations to an organization. In order to list invitations to an
        organization, the authenticated user must be a member or an admin of
        the organization.

        **Example request**:

        .. sourcecode:: http

            GET /organizations/1/invitations HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'code': '12345678-1234-1234-1234-123456789012',
                    'email': 'john@example.org',
                    'status': 'pending',
                    'organization_id': 1
                }
            ]

        :param int organization_id: the organization the invitations are
                                    listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the invitation's unique id
        :>jsonarr string code: the invitation's unique code
        :>jsonarr string email: the email address the invitation is sent to
        :>jsonarr string status: the invitation's status
        :>jsonarr int organization_id: the organization the invitation is
                                       related to

        :status 200: Invitations are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Organization is not found

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            abort(404)

        invitations = InvitationModel.query.filter_by(
            organization_id=organization.id)

        data = [i.serialize for i in invitations]

        return data, 200
