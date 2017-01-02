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
        Retrieve an accountability.

        Request:
            GET /accountabilities/{accountability_id}

        Response:
            200 OK - If accountability is retrieved
                {
                    'id': 1,
                    'title': 'Accountability\'s title'
                    'role_id': 99
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If accountability is not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        return accountability.serialize, 200

    @auth.login_required
    def put(self, accountability_id):
        """
        Update an accountability.

        Request:
            PUT /accountabilities/{accountability_id}

            Parameters:
                title (string): The new title of the accountability

        Response:
            200 OK - If accountability is updated
                {
                    'id': 1,
                    'title': 'Accountability\'s title',
                    'role_id': 99
                }
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If accountability is not found

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
        Delete an accountability.

        Request:
            DELETE /accountabilities/{accountability_id}

        Response:
            204 No Content - If the accountability was deleted
            400 Bad Request - If token is not well-formed
            401 Unauthorized - If token has expired
            401 Unauthorized - If user is not authorized
            404 Not Found - If accountability is not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        db.session.delete(accountability)
        db.session.commit()

        return None, 204
