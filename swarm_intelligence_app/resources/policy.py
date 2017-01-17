"""
Define the classes for the policy API.

"""
from flask import abort
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
        .. :quickref: Policy; Retrieve a policy.

        Retrieve a policy.

        **Example request**:

        .. sourcecode:: http

            GET /policies/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Policy\'s title',
                'domain_id': 1
            }

        :param int policy_id: the policy to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the policy's unique id
        :>json string title: the policy's title
        :>json int domain_id: the domain the policy is related to

        :status 200: Policy is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Policy is not found

        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            abort(404)

        return policy.serialize, 200

    @auth.login_required
    def put(self, policy_id):
        """
        .. :quickref: Policy; Update a policy.

        Update a policy.

        **Example request**:

        .. sourcecode:: http

            PUT /policies/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Policy\'s new title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Policy\'s new title',
                'domain_id': 1
            }

        :param int policy_id: the policy to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the policy's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the policy's unique id
        :>json string title: the policy's title
        :>json int domain_id: the domain the policy is related to

        :status 200: Policy is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Policy is not found

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
        .. :quickref: Policy; Delete a policy.

        Delete a policy.

        **Example request**:

        .. sourcecode:: http

            DELETE /policies/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int policy_id: the policy to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Policy is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Policy is not found

        """
        policy = PolicyModel.query.get(policy_id)

        if policy is None:
            abort(404)

        db.session.delete(policy)
        db.session.commit()

        return None, 204
