"""
Define the classes for the partner API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
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
            raise errors.EntityNotFoundError('partner', partner_id)

        return {
            'success': True,
            'data': partner.serialize
        }, 200

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
        }, 200

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
            raise errors.EntityNotFoundError('partner', partner_id)

        partner.is_deleted = True
        db.session.commit()

        return {
            'success': True,
            'data': partner.serialize
        }, 200


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
                raise errors.EntityNotFoundError('partner', partner_id)

            partner.type = PartnerType.ADMIN
            db.session.commit()

            return {
                'success': True,
                'data': partner.serialize
            }, 200

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
                raise errors.EntityNotFoundError('partner', partner_id)

            partner.type = PartnerType.MEMBER
            db.session.commit()

            return {
                'success': True,
                'data': partner.serialize
            }, 200


class PartnerCircles(Resource):
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
            raise errors.EntityNotFoundError('partner', partner_id)

        data = [i.serialize for i in partner.circles]
        return {
            'success': True,
            'data': data
        }, 200


class PartnerMetrics(Resource):
    """
    Define the endpoints for the metrics edge of the partner node.

    """
    def post(self,
             partner_id):
        """
        Add a metric to a partner.

        """
        raise errors.MethodNotImplementedError()

    def get(self,
            partner_id):
        """
        List metrics of a partner.

        """
        raise errors.MethodNotImplementedError()


class PartnerChecklists(Resource):
    """
    Define the endpoints for the checklists edge of the partner node.

    """
    def post(self,
             partner_id):
        """
        Add a checklist to a partner.

        """
        raise errors.MethodNotImplementedError()

    def get(self,
            partner_id):
        """
        List checklists of a partner.

        """
        raise errors.MethodNotImplementedError()


class PartnerRoles(Resource):
    """
    Define the endpoints for the role edge of the partner node.

    """

    @auth.login_required
    def get(self, partner_id):
        """
        List all roles of a partner.

        Args:
            partner_id: The id of the partner for which to list the circles.

        Body:

        Headers:
            Authorization: A string of the authorization token.

        Return:
            A dictionary mapping keys to the corresponding table row data
            fetched and converted to json. Each row is represented as a
            tuple of strings. For example:
            {
                'success': True,
                'data': {
                        'circle_id': '3',
                        'id': '2',
                        'name': 'Manager',
                        'parent_circle_id': 2,
                        'purpose': 'Purpose of the Role',
                        'type': 'custom'
                        }
            }
            {
                'success': False,
                'errors': [{
                            'type': 'EntityNotFoundError',
                            'message': 'The circle with id 1 does not exist'
                        }]
            }

        Raises:
            EntityNotFoundError: There is no entry found with the id.
        """
        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            raise errors.EntityNotFoundError('circle', partner_id)

        data = [i.serialize for i in partner.roles]
        return {
                   'success': True,
                   'data': data
               }, 200
