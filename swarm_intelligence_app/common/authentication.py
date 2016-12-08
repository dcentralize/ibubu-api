"""
Define any authentication functions for the application.

"""
import jwt
from flask import abort, g
from flask_httpauth import HTTPTokenAuth
from swarm_intelligence_app.models.user import User as UserModel

APP_SECRET = 'top_secret'

auth = HTTPTokenAuth('Bearer')

mock_users = {
    'mock_user_001': {
        'google_id': 'mock_user_001',
        'firstname': 'Donald',
        'lastname': 'Duck',
        'email': 'donald@gmail.de'
    },
    'mock_user_002': {
        'google_id': 'mock_user_002',
        'firstname': 'Dagobert',
        'lastname': 'Duck',
        'email': 'dagobert@gmail.de'
    }
}


def get_mock_user():
    return mock_users


@auth.verify_token
def verify_token(token):
    """
    Validate a JSON Web Token.

    """
    try:
        payload = jwt.decode(token, APP_SECRET)
    except jwt.ExpiredSignatureError:
        print('The access token has expired.')
        abort(401)
    except jwt.exceptions.InvalidTokenError:
        print('The access token is not valid.')
        abort(400)

    user = UserModel.query.filter_by(
        google_id=payload['sub'], is_deleted=False).first()

    if user is None:
        print('The user is not found or is deleted.')
        abort(401)

    g.user = user

    return True
