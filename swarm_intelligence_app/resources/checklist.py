from flask_restful import Resource
from swarm_intelligence_app.common import errors


class Checklist(Resource):
    def get(self,
            checklist_id):
        """
        Retrieve a checklist
        """
        raise errors.MethodNotImplementedError()

    def put(self,
            checklist_id):
        """
        Edit a checklist
        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               checklist_id):
        """
        Delete a checklist
        """
        raise errors.MethodNotImplementedError()
