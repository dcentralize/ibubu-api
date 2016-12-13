"""
Define the classes for the accountability API.

"""
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
            200 OK - If the accountability was retrieved
                {
                    'id': '1',
                    'title': 'The title of the accountability'
                    'role_id': '99'
                }
            404 Not Found - If the accountability was not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        return accountability.serialize, 200

    @auth.login_required
    def put(self, accountability_id):
        """
        Edit an accountability.

        Request:
            PUT /accountabilities/{accountability_id}

            Parameters:
                title (string): The new title of the accountability

        Response:
            200 OK - If accountability was updated
                {
                    'id': 1,
                    'title': 'The new title of the accountability',
                    'role_id': 99
                }
            404 Not Found - If accountability was not found

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
            404 Not found - If the accountability was not found

        """
        accountability = AccountabilityModel.query.get(accountability_id)

        if accountability is None:
            abort(404)

        db.session.delete(accountability)
        db.session.commit()

        return None, 204
