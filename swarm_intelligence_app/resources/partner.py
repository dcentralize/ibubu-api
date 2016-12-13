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

        Args:
            partner_id: The id of the partner to retrieve

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        return partner.serialize, 200

    @auth.login_required
    def put(self,
            partner_id):
        """
        Edit a partner.

        In order to edit a partner, the authenticated user must be an admin of
        the organization that the partner is associated with.

        Args:
            partner_id: The id of the partner to edit

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

        Args:
            partner_id: The id of the partner to delete

        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        partner.is_deleted = True
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

            Args:
                partner_id: The id of the partner to grant admin access to

            """
            partner = PartnerModel.query.get(partner_id)

            if partner is None:
                abort(404)

            partner.type = PartnerType.admin
            db.session.commit()

            return partner.serialize, 200

        @auth.login_required
        def delete(self,
                   partner_id):
            """
            Revoke admin access from a partner to an organization.

            In order to revoke admin access from a partner to an organization,
            the authenticated user must be an admin of the organization that
            the partner is associated with.

            Args:
                partner_id: The id of the partner to revoke admin access from

            """
            partner = PartnerModel.query.get(partner_id)

            if partner is None:
                abort(404)

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

        Args:
            partner_id: The id of the partner for which to list the circles

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
