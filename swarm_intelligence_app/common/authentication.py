"""
Define any authentication functions for the application.

"""
import requests
from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')

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


@auth.verify_token
def verify_token(token):
    """
    Validate a google id token.

    """
    if token == 'mock_user_001' or 'mock_user_002':
        g.user = mock_users[token]
        return True
    else:
        response = requests.get('https://www.googleapis.com/oauth2/v3/'
                                'tokeninfo?id_token=' + token)

        if response.status_code != 200:
            return False

        data = response.json()
        if data['aud'] != '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54' \
                          '.apps.googleusercontent.com':
            return False

        g.user = {
            'google_id': data['sub'],
            'firstname': data['given_name'],
            'lastname': data['family_name'],
            'email': data['email']
        }

        return True
