from flask_restful import Resource, reqparse
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth


class Partner(Resource):
    # get a partner
    # permissions: login_required, organization_partner
    @auth.login_required
    def get(self, partner_id):
        partner = PartnerModel.query.get(partner_id)
        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)
        return {
            'success': True,
            'data': partner.serialize
        }

    # update a partner
    # permissions: login_required, partner_owner
    @auth.login_required
    def put(self, partner_id):
        partner = PartnerModel.query.get(partner_id)
        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('firstname', required=True)
        parser.add_argument('lastname', required=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        partner.firstname = args['firstname']
        partner.lastname = args['lastname']
        partner.email = args['email']
        db.session.commit()

        return {
            'success': True,
            'data': partner.serialize
        }


class PartnerMetrics(Resource):
    # create a new metric for a partner
    # permissions: login_required, organization_partner
    def post(self, partner_id):
        raise errors.MethodNotImplementedError()

    # get a list of metrics of a partner
    # permissions: login_required, organization_partner
    def get(self, partner_id):
        raise errors.MethodNotImplementedError()


class PartnerChecklists(Resource):
    # create a new checklist for a partner
    # permissions: login_required, organization_partner
    def post(self, partner_id):
        raise errors.MethodNotImplementedError()

    # get a list of checklists of a partner
    # permissions: login_required, organization_partner
    def get(self, partner_id):
        raise errors.MethodNotImplementedError()
