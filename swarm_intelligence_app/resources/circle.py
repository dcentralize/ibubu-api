"""
Define the classes for the circle API.

"""
from flask_restful import Resource
from swarm_intelligence_app.common import errors


class Circle(Resource):
    """
    Define the endpoints for the circle node.

    """
    def get(self,
            circle_id):
        """
        Retrieve a circle.

        """
        raise errors.MethodNotImplementedError()

    def put(self,
            circle_id):
        """
        Edit a circle.

        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               circle_id):
        """
        Delete a circle.

        """
        raise errors.MethodNotImplementedError()


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
