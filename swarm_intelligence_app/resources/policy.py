"""
Define the classes for the policy API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.policy import Policy as \
     PolicyModel


class Policy(Resource):
    """
    Define the endpoints for the policy node.

    """
    @auth.login_required
    def get(self, policy_id):
        """
        Retrieve a accountability.

        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            abort(404)

        return policy.serialize, 200

    @auth.login_required
    def put(self, policy_id):
        """
        Edit a policy.

        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        args = parser.parse_args()

        policy.title = args['title']
        policy.description = args['descrition']
        db.session.commit()

        return policy.serialize, 200

    @auth.login_required
    def delete(self, policy_id):
        """
        Delete a policy.

        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            abort(404)

        db.session.delete(policy)
        db.session.commit()

        return None, 204
