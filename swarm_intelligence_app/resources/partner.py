"""
Define the classes for the partner API.

"""
from flask import abort
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType


class Partner(Resource):
    """
    Define the endpoints for the partner node.

    """
    @auth.login_required
    def get(self,
            partner_id):
        """
        .. :quickref: Partner; Retrieve a partner.

        Retrieve a partner.

        In order to retrieve a partner, the authenticated user must be a
        partner of the organization that the partner is associated with.

        **Example request**:

        .. sourcecode:: http

            GET /partners/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

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

        :param int partner_id: the partner to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the partner's unique id
        :>json string type: the partner's type
        :>json string firstname: the partner's firstname
        :>json string lastname: the partner's lastname
        :>json string email: the partner's email address
        :>json boolean is_active: the partner's status
        :>json int user_id: the user account the partner is related to
        :>json int organization_id: the organization the partner is related to
        :>json int invitation_id: the invitation the partner is related to

        :status 200: Partner is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        return partner.serialize, 200

    @auth.login_required
    def put(self,
            partner_id):
        """
        .. :quickref: Partner; Update a partner.

        Update a partner.

        In order to update a partner, the authenticated user must be a partner
        with admin access of the organization that the partner is associated
        with.

        **Example request**:

        .. sourcecode:: http

            PUT /partners/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'firstname': 'John',
                'lastname': 'Doe',
                'email': 'john@example.org'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

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

        :param int partner_id: the partner to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string firstname: the partner's firstname
        :<json string lastname: the partner's lastname
        :<json string email: the partner's email address

        :resheader Content-Type: data is received as application/json

        :>json int id: the partner's unique id
        :>json string type: the partner's type
        :>json string firstname: the partner's firstname
        :>json string lastname: the partner's lastname
        :>json string email: the partner's email address
        :>json boolean is_active: the partner's status
        :>json int user_id: the user account the partner is related to
        :>json int organization_id: the organization the partner is related to
        :>json int invitation_id: the invitation the partner is related to

        :status 200: Partner is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('firstname', required=True)
        parser.add_argument('lastname', required=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        partner.firstname = args['firstname']
        partner.lastname = args['lastname']
        partner.email = args['email']
        db.session.commit()

        return partner.serialize, 200

    @auth.login_required
    def delete(self,
               partner_id):
        """
        .. :quickref: Partner; Delete a partner.

        Delete a partner.

        In order to delete a partner, the authenticated user must be a partner
        with admin access of the organization that the partner is associated
        with.

        **Example request**:

        .. sourcecode:: http

            DELETE /partners/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int partner_id: the partner to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Partner is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found
        :status 409: Partner is the only admin of an organization

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        if partner.type == PartnerType.admin and partner.is_active is True:
            admins = PartnerModel.query.filter_by(
                organization_id=partner.organization_id,
                type=PartnerType.admin,
                is_active=True).all()

            if len(admins) <= 1:
                abort(409, 'Cannot delete partner. There must be at least one '
                           'admin of an organization.')

        partner.is_active = False
        db.session.commit()

        return None, 204


class PartnerAdmin(Resource):
    """
    Define the endpoints for the admin edge of the partner node.

    """
    @auth.login_required
    def put(self,
            partner_id):
        """
        .. :quickref: Partner Admin; Grant admin access.

        Grant admin access to a partner.

        In order to grant admin access to an organization to a partner, the
        authenticated user must be an admin of the organization that the
        partner is associated with.

        **Example request**:

        .. sourcecode:: http

            PUT /partners/1/admin HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int partner_id: the partner to grant access to an organization

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Admin access is grant
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        partner.type = PartnerType.admin
        db.session.commit()

        return None, 204

    @auth.login_required
    def delete(self,
               partner_id):
        """
        .. :quickref: Partner Admin; Revoke admin access.

        Revoke admin access to an organization from a partner.

        In order to revoke admin access to an organization from a partner,
        the authenticated user must be an admin of the organization that
        the partner is associated with.

        **Example request**:

        .. sourcecode:: http

            DELETE /partners/1/admin HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int partner_id: the partner to revoke access to an organization

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Admin access is revoked
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found
        :status 409: Partner is the only admin of an organization

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        if partner.type == PartnerType.admin and partner.is_active is True:
            admins = PartnerModel.query.filter_by(
                organization_id=partner.organization_id,
                type=PartnerType.admin,
                is_active=True).all()

            if len(admins) <= 1:
                abort(409, 'Cannot delete partner. There must be at least one '
                           'admin of an organization.')

        partner.type = PartnerType.member
        db.session.commit()

        return None, 204


class PartnerMemberships(Resource):
    """
    Define the endpoints for the circles edge of the partner node.

    """
    def get(self,
            partner_id):
        """
        .. :quickref: Partner Memberships; List memberships of a partner.

        List memberships of a partner.

        In order to list the memberships of a partner, the authenticated user
        must be a partner of the organization that the partner is associated
        with.

        **Example request**:

        .. sourcecode:: http

            GET /partners/1/memberships HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'type': 'circle',
                    'name': 'My Organization',
                    'pupose': 'My Organization\'s purpose',
                    'parent_role_id': null,
                    'organization_id': 1
                },
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

        :param int partner_id: the partner the memberships are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the role's unique id
        :>jsonarr string type: the role's type
        :>jsonarr string name: the role's name
        :>jsonarr string purpose: the role's purpose
        :>jsonarr int parent_role_id: the parent role the role is related to
        :>jsonarr int organization_id: the organization the role is related to

        :status 200: Memberships are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Partner is not found

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        data = [i.serialize for i in partner.memberships]

        return data, 200


class PartnerMetrics(Resource):
    """
    Define the endpoints for the metrics edge of the partner node.

    """
    def post(self,
             partner_id):
        """
        .. :quickref: Partner Metrics; Add a metric to a partner.
          :noindex:

        """
        abort(501)

    def get(self,
            partner_id):
        """
        .. :quickref: Partner Metrics; List metrics of a partner.
          :noindex:

        """
        abort(501)


class PartnerChecklists(Resource):
    """
    Define the endpoints for the checklists edge of the partner node.

    """
    def post(self,
             partner_id):
        """
        .. :quickref: Partner Checklists; Add a checklist to a partner.
          :noindex:

        """
        abort(501)

    def get(self,
            partner_id):
        """
        .. :quickref: Partner Checklists; List checklists of a partner.
          :noindex:

        """
        abort(501)
