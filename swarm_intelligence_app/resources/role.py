"""
Define the classes for the role API.

"""
from flask_restful import Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.models.role import Role as RoleModel


class Role(Resource):
    """
    Define the endpoints for the role node.

    """
    def get(self, role_id):
        """
        Retrieve a role.

        """
        # ToDO
        role = RoleModel.query.get(role_id)
        print(role)
        raise errors.MethodNotImplementedError()

    def put(self, role_id):
        """
        Edit a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()

    def delete(self, role_id):
        """
        Delete a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()


class RoleMembers(Resource):
    """
    Define the endpoints for the members edge of the role node.

    """
    def get(self, role_id):
        """
        List members of a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()

    def put(self, role_id, partner_id):
        """
        Assign a partner to a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()

    def delete(self, role_id, partner_id):
        """
        Unassign a partner from a role.

        """
        # ToDO
        raise errors.MethodNotImplementedError()


class RoleCircle(Resource):
    """
    Define the endpoints for the circle edge of the role node.

    """
    def put(self, role_id):
        """
        Update the role to a circle.

        """
        # ToDO
        raise errors.MethodNotImplementedError()
