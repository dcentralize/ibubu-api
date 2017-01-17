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
        .. :quickref: Domain; Retrieve a domain.

        Retrieve a domain.

        **Example request**:

        .. sourcecode:: http

            GET /domains/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Domain\'s title',
                'role_id': 1
            }

        :param int domain_id: the domain to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the domain's unique id
        :>json string title: the domain's title
        :>json int role_id: the role the domain is related to

        :status 200: Domain is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Domain is not found

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        return domain.serialize, 200

    @auth.login_required
    def put(self, domain_id):
        """
        .. :quickref: Role; Update a domain.

        Update a domain.

        **Example request**:

        .. sourcecode:: http

            PUT /domains/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Domain\'s new title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Domain\'s new title',
                'role_id': 1
            }

        :param int domain_id: the domain to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the domain's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the domain's unique id
        :>json string title: the domain's title
        :>json int role_id: the domain the role is related to

        :status 200: Domain is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Domain is not found

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
        .. :quickref: Domain; Delete a domain.

        Delete a domain.

        **Example request**:

        .. sourcecode:: http

            DELETE /domain/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int domain_id: the domain to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Domain is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Domain is not found

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
        .. :quickref: Domain Policies; List policies of a domain.

        List policies of a domain.

        **Example request**:

        .. sourcecode:: http

            GET /domains/1/policies HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'title': 'Policy\'s title',
                    'domain_id': 1
                }
            ]

        :param int domain_id: the domain the policies are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the policy's unique id
        :>jsonarr string title: the policy's title
        :>jsonarr int domain_id: the domain the policy is related to

        :status 200: Policies are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Domain is not found

        """
        domain = DomainModel.query.get(domain_id)

        if domain is None:
            abort(404)

        data = [i.serialize for i in domain.policies]

        return data, 200

    @auth.login_required
    def post(self, domain_id):
        """
        .. :quickref: Domain Policies; Add a policy to a domain.

        Add a policy to a domain.

        **Example request**:

        .. sourcecode:: http

            POST /domains/1/policies HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Policy\'s title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Policy\'s title',
                'domain_id': 1
            }

        :param int organization_id: the domain the policy is added to

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string title: the policy's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the policy's unique id
        :>json string title: the policy's title
        :>json int domain_id: the domain the policy is related to

        :status 201: Policy is added to domain
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Domain is not found

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
