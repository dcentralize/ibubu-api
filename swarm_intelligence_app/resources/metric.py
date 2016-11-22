from flask_restful import Resource
from swarm_intelligence_app.common import errors


class Metric(Resource):
    def get(self,
            metric_id):
        """
        Retrieve a metric
        """
        raise errors.MethodNotImplementedError()

    def put(self,
            metric_id):
        """
        Edit a metric
        """
        raise errors.MethodNotImplementedError()

    def delete(self,
               metric_id):
        """
        Delete a metric
        """
        raise errors.MethodNotImplementedError()
