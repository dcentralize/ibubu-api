"""
Define the classes for the domain API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.domain import Domain as \
     DomainModel
from swarm_intelligence_app.models.policy import Policy as PolicyModel


class Domain(Resource):
    """
    Define the endpoints for the domain node.

    """
    @auth.login_required
    def get(self, domain_id):
        """
        Retrieve a domain.

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        return domain.serialize, 200

    @auth.login_required
    def put(self, domain_id):
        """
        Edit a domain.

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        domain.title = args['title']
        db.session.commit()

        return domain.serialize, 200

    @auth.login_required
    def delete(self, domain_id):
        """
        Delete a policy.

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        db.session.delete(domain)
        db.session.commit()

        return None, 204


class DomainPolicies(Resource):
    """
    Define the endpoints for the policy edge of the domain node.

    """
    @auth.login_required
    def get(self, domain_id):
        """
        List of all policies of a domain.

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        data = [i.serialize for i in domain.policies]

        return data, 200

    @auth.login_required
    def post(self, domain_id):
        """
        Create a new policy for the domain.

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        args = parser.parse_args()

        policy = PolicyModel(args['title'], args['description'], domain.id)
        domain.policies.append(policy)
        db.session.commit()

        return policy.serialize, 201
