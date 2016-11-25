"""
Define the classes for the circle API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel


class Circle(Resource):
    """
    Define the endpoints for the circle node.

    """
    def get(self,
            circle_id):
        """
        Retrieve a circle.

        In order to retrieve a circle, the authenticated user must be a member
        or an admin of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to retrieve

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        return {
            'success': True,
            'data': circle.serialize
        }, 200

    def put(self,
            circle_id):
        """
        Edit a circle.

        In order to edit a circle, the authenticated user must be an admin
        of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to edit

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose')
        parser.add_argument('strategy')
        args = parser.parse_args()

        circle.name = args['name']
        circle.purpose = args['purpose']
        circle.strategy = args['strategy']
        db.session.commit()

        return {
            'success': True,
            'data': circle.serialize
        }, 200

    def delete(self,
               circle_id):
        """
        Delete a circle.

        In order to delete a circle, the authenticated user must be an admin
        of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to delete

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        db.session.delete(circle)
        db.session.commit()

        return {
            'success': True
        }


class CircleSubcircles(Resource):
    """
    Define the endpoints for the subcircles edge of the circle node.

    """
    def post(self,
             circle_id):
        """
        Add a subcircle to a circle.

        In order to add a subcircle to a circle, the authenticated user must
        be an admin of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to add the subcircle to

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose')
        parser.add_argument('strategy')
        args = parser.parse_args()

        subcircle = CircleModel(args['name'], args['purpose'],
                                args['strategy'], circle.organization_id,
                                circle.id)
        db.session.add(subcircle)
        db.session.commit()

        return {
            'success': True,
            'data': subcircle.serialize
        }, 200

    def get(self,
            circle_id):
        """
        List subcircles of a circle.

        In order to list the subcircles of a circle, the authenticated user
        must be a member or an admin of the organization that the circle is
        associated with.

        Args:
            circle_id: The id of the circle for which to list the subcircles

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        subcircles = CircleModel.query.filter_by(circle_id=circle.id).all()

        data = [i.serialize for i in subcircles]
        return {
            'success': True,
            'data': data
        }, 200


class CircleRoles(Resource):
    """
    Define the endpoints for the roles edge of the circle node.

    """
    def post(self,
             circle_id):
        """
        Add a role to a circle.

        """
        raise errors.MethodNotImplementedError()

    def get(self,
            circle_id):
        """
        List roles of a circle.

        """
        raise errors.MethodNotImplementedError()


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

        Args:
            circle_id: The id of the circle for which to list the members

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        data = [i.serialize for i in circle.partners]
        return {
            'success': True,
            'data': data
        }

        raise errors.MethodNotImplementedError()

    def put(self,
            circle_id,
            partner_id):
        """
        Assign a partner to a circle.

        In order to assign a partner to a circle, the authenticated user must
        be an admin of the organization that the circle is associated with.

        Args:
            circle_id: The id of the circle to assign the partner to
            partner_id: The id of the partner to assign

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)

        circle.partners.append(partner)
        db.session.commit()

        return {
            'success': True
        }, 200

    def delete(self,
               circle_id,
               partner_id):
        """
        Unassign a partner from a circle.

        In order to unassign a partner from a circle, the authenticated user
        must be an admin of the organization that the circle is associated
        with.

        Args:
            circle_id: The id of the circle to unassign the partner from
            partner_id: The id of the partner to unassign

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None:
            raise errors.EntityNotFoundError('circle', circle_id)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            raise errors.EntityNotFoundError('partner', partner_id)

        circle.partners.remove(partner)
        db.session.commit()

        return {
            'success': True
        }, 200
