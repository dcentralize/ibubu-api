from flask_restful import Resource
from swarm_intelligence_app.common import errors

class Circle(Resource):
    # get a circle
    # permissions: login_required
    def get(self, circle_id):
        raise errors.MethodNotImplementedError()

    # update a circle
    # permissions: login_required
    def put(self, circle_id):
        raise errors.MethodNotImplementedError()

    # delete a circle
    # permissions: login_required
    def delete(self, circle_id):
        raise errors.MethodNotImplementedError()

class CircleRoles(Resource):
    # create a new role within a circle
    # permissions: login_required
    def post(self, circle_id):
        raise errors.MethodNotImplementedError()

    # get a list of roles of a circle
    # permissions: login_required
    def get(self, circle_id):
        raise errors.MethodNotImplementedError()

class CircleMembers(Resource):
    # assign a member to a circle
    # permissions: login_required
    def post(self, circle_id):
        raise errors.MethodNotImplementedError()

    # get a list of members assigned to a circle
    # permissions: login_required
    def get(self, circle_id):
        raise errors.MethodNotImplementedError()

    # unassign a member from a circle
    # permissions: login_required
    def delete(self, circle_id):
        raise errors.MethodNotImplementedError()