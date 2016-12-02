"""
Define any authentication functions for the application.

"""
import jwt
from flask import abort, g
from flask_httpauth import HTTPTokenAuth
from swarm_intelligence_app.models.user import User as UserModel

APP_SECRET = 'top_secret'

auth = HTTPTokenAuth('Bearer')


@auth.verify_token
def verify_token(token):
    """
    Validate a JSON Web Token.

    """
    try:
        payload = jwt.decode(token, APP_SECRET)
    except jwt.ExpiredSignatureError:
        abort(401)
    except jwt.exceptions.InvalidTokenError:
        abort(400)

    user = UserModel.query.filter_by(
        google_id=payload['sub'], is_deleted=False).first()

    if user is None:
        abort(401)

    g.user = user

    return True
