"""
Define the classes for the circle API.

"""
from flask_restful import reqparse, Resource

from swarm_intelligence_app.common import errors
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models import db
from swarm_intelligence_app.common.authentication import auth


class Circle(Resource):
    """
    Define the endpoints for the circle node.

    """

    @auth.login_required
    def get(self, circle_id):
        """
        Retrieve a circle.

        """
        circle = CircleModel.query.get(circle_id)

        if circle is None or circle.is_deleted:
            raise errors.EntityNotFoundError('circle', circle_id)

        return {
                   'success': True,
                   'data': circle.serialize
               }, 200

    def put(self, circle_id):
        """
        Edit a circle.
        """
        circle = CircleModel.query.get(circle_id)
        if circle is None or circle.is_deleted:
            raise errors.EntityNotFoundError('circle', circle_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        circle.name = args['name']
        db.session.commit()

        return {
                   'success': True,
                   'data': circle.serialize
               }, 200

    def delete(self, circle_id):
        """
        Delete a circle.
        """
        circle = CircleModel.query.get(circle_id)
        if circle is None or circle.is_deleted:
            raise errors.EntityNotFoundError('circle', circle_id)
        circle.is_deleted = True

        for circle in circle.child_circles:
            circle.is_deleted = True

        db.session.commit()
        return {
                   'success': True,
                   'data': circle.serialize
               }, 200


class CircleRoles(Resource):
    """
    Define the endpoints for the roles edge of the circle node.

    """

    def post(self, circle_id):
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

        """
        raise errors.MethodNotImplementedError()

    def put(self,
            circle_id,
            partner_id):
        """
        Assign a partner to a circle.

        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               circle_id,
               partner_id):
        """
        Unassign a partner from a circle.

        """
        raise errors.MethodNotImplementedError()
