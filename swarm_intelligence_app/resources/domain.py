"""
Define the classes for the domain API.

"""
from flask import abort
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

        Request:
            GET /domains/{domain_id}

        Response:
            200 OK - If domain is retrieved
                {
                    'id': 1,
                    'title': 'Domain\'s title'
                    'role_id': 99
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If domain is not found

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        return domain.serialize, 200

    @auth.login_required
    def put(self, domain_id):
        """
        Update a domain.

        Request:
            PUT /domains/{domain_id}

            Parameters:
                title (string): The new title of the domain

        Response:
            200 OK - If domain is updated
                {
                    'id': 1,
                    'title': 'Domain\'s title',
                    'role_id': 99
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If domain is not found

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
        Delete a domain.

        Request:
            DELETE /domains/{domain_id}

        Response:
            204 No Content - If the domain is deleted
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If domain is not found

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

        Request:
            GET /domains/{domain_id}/policies

        Response:
            200 OK - If policies of domain are listed
                [
                    {
                        'id': 1,
                        'title': 'Policy\'s name',
                        'description': 'Policy\'s description',
                        'domain_id': 1
                    }
                ]
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If domain is not found

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        data = [i.serialize for i in domain.policies]

        return data, 200

    @auth.login_required
    def post(self, domain_id):
        """
        Add a policy to a domain.

        Request:
            POST /domains/{domain_id}/policies

            Parameters:
                title (string): The title of the policy
                description (string): The description of the policy

        Response:
            201 Created - If policy is added
                {
                    'id': 1,
                    'title': 'Policy\'s title',
                    'description': 'Policy\'s description',
                    'domain_id': 1
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If domain is not found

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
