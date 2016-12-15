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
        Retrieve a partner.

        In order to retrieve a partner, the authenticated user must be a
        member or an admin of the organization that the partner is
        associated with.

        Request:
            GET /partners/{partner_id}

        Response:
            200 OK - If partner is retrieved
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
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If partner is not found

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        return partner.serialize, 200

    @auth.login_required
    def put(self,
            partner_id):
        """
        Update a partner.

        In order to edit a partner, the authenticated user must be an admin of
        the organization that the partner is associated with.

        Request:
            PUT /partners/{partner_id}

            Parameters:
                firstname (string): The firstname of the partner
                lastname (string): The lastname of the partner
                email (string): The email address of the partner

        Response:
            200 OK - If partner is updated
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
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If partner is not found

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
        Delete a partner.

        In order to delete a partner, the authenticated user must be an admin
        of the organization that the partner is associated with.

        Request:
            DELETE /partners/{partner_id}

        Response:
            204 No Content - If partner is deleted
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not found - If partner is not found
            409 Conflict - If partner is the only admin of an organization

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
        Grant admin access to a partner to an organization.

        In order to grant admin access to a partner to an organization,
        the authenticated user must be an admin of the organization that
        the partner is associated with.

        Request:
            PUT /partners/{partner_id}/admin

        Response:
            204 No Content - If admin access is grant to partner
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If partner is not found

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
        Revoke admin access from a partner to an organization.

        In order to revoke admin access from a partner to an organization,
        the authenticated user must be an admin of the organization that
        the partner is associated with.

        Request:
            DELETE /partners/{partner_id}/admin

        Response:
            204 No Content - If admin access is revoked from partner
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If partner is not found
            409 Conflict - If partner is the only admin of an organization

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
        List circles of a partner.

        In order to list the circles of a partner, the authenticated user
        must be a member or an admin of the organization that the partner is
        associated with.

        Request:
            GET /partners/{partner_id}/memberships

        Response:
            200 OK - If memberships of partner are listed
                [
                    {
                        'id': 1,
                        'type': 'circle|lead_link|secretary|facilitator|
                         custom',
                        'name': 'Role\'s name',
                        'purpose': 'Role\'s purpose',
                        'strategy': 'null|Role\'s strategy',
                        'parent_circle_id': 1,
                        'organization_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If partner is not found

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
        Add a metric to a partner.

        """
        abort(501)

    def get(self,
            partner_id):
        """
        List metrics of a partner.

        """
        abort(501)


class PartnerChecklists(Resource):
    """
    Define the endpoints for the checklists edge of the partner node.

    """
    def post(self,
             partner_id):
        """
        Add a checklist to a partner.

        """
        abort(501)

    def get(self,
            partner_id):
        """
        List checklists of a partner.

        """
        abort(501)
