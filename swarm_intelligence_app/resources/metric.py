"""
Define the classes for the metric API.

"""
from flask import abort
from flask_restful import Resource


class Metric(Resource):
    """
    Define the endpoints for the metric node.

    """
    def get(self,
            metric_id):
        """
        Retrieve a metric.

        """
        abort(501)

    def put(self,
            metric_id):
        """
        Edit a metric.

        """
        abort(501)

    def delete(self,
               metric_id):
        """
        Delete a metric.

        """
        abort(501)
