"""
Define the classes for the checklist API.

"""

from flask import abort
from flask_restful import Resource


class Checklist(Resource):
    """
    Define the endpoints for the checklist node.

    """
    def get(self,
            checklist_id):
        """
        Retrieve a checklist.

        """
        abort(501)

    def put(self,
            checklist_id):
        """
        Edit a checklist.

        """
        abort(501)

    def delete(self,
               checklist_id):
        """
        Delete a checklist.

        """
        abort(501)
