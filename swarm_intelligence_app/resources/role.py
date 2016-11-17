from flask_restful import Resource
from swarm_intelligence_app.common import errors


class Role(Resource):
    # get a role
    # permissions: login_required
    def get(self, role_id):
        raise errors.MethodNotImplementedError()

    # update a role
    # permissions: login_required
    def put(self, role_id):
        raise errors.MethodNotImplementedError()

    # delete a role
    # permissions: login_required
    def delete(self, role_id):
        raise errors.MethodNotImplementedError()


class RoleMembers(Resource):
    # assign a member to a role
    # permissions: login_required
    def post(self, role_id):
        raise errors.MethodNotImplementedError()

    # get a list of members assigned to a role
    # permissions: login_required
    def get(self, role_id):
        raise errors.MethodNotImplementedError()

    # unassign a member from a role
    # permissions: login_required
    def delete(self, role_id):
        raise errors.MethodNotImplementedError()
