"""
Define the classes for the role API.

"""
from flask_restful import Resource
from swarm_intelligence_app.common import errors


class Role(Resource):
    """
    Define the endpoints for the role node.

    """
    def get(self,
            role_id):
        """
        Retrieve a role.

        """
        raise errors.MethodNotImplementedError()

    def put(self,
            role_id):
        """
        Edit a role.

        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               role_id):
        """
        Delete a role.

        """
        raise errors.MethodNotImplementedError()


class RoleMembers(Resource):
    """
    Define the endpoints for the members edge of the role node.

    """
    def get(self,
            role_id):
        """
        List members of a role.

        """
        raise errors.MethodNotImplementedError()

    def put(self,
            role_id,
            partner_id):
        """
        Assign a partner to a role.

        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               role_id,
               partner_id):
        """
        Unassign a partner from a role.

        """
        raise errors.MethodNotImplementedError()
