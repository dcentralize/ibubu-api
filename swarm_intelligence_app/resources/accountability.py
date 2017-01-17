"""
Define the classes for the accountability API.

"""
from flask import abort
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.accountability import Accountability as \
    AccountabilityModel


class Accountability(Resource):
    """
    Define the endpoints for the accountability node.

    """
    @auth.login_required
    def get(self, accountability_id):
        """
        .. :quickref: Accountability; Retrieve an accountability.

        Retrieve an accountability.

        **Example request**:

        .. sourcecode:: http

            GET /accountabilities/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Accountability\'s title',
                'role_id': 1
            }

        :param int accountability_id: the accountability to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the accountability's unique id
        :>json string title: the accountability's title
        :>json int role_id: the role the accountability is related to

        :status 200: Accountability is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Accountability is not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        return accountability.serialize, 200

    @auth.login_required
    def put(self, accountability_id):
        """
        .. :quickref: Accountability; Update an accountability.

        Update an accountability.

        **Example request**:

        .. sourcecode:: http

            PUT /accountabilities/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Accountability\'s new title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Accountability\'s new title',
                'role_id': 1
            }

        :param int accountability_id: the accountability to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the accountability's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the accountability's unique id
        :>json string title: the accountability's title
        :>json int role_id: the role the accountability is related to

        :status 200: Accountability is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Accountability is not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        accountability.title = args['title']
        db.session.commit()

        return accountability.serialize, 200

    @auth.login_required
    def delete(self, accountability_id):
        """
        .. :quickref: Accountability; Delete an accountability.

        Delete an accountability.

        **Example request**:

        .. sourcecode:: http

            DELETE /accountabilities/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int accountability_id: the accountability to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Accountability is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Accountability is not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        db.session.delete(accountability)
        db.session.commit()

        return None, 204
