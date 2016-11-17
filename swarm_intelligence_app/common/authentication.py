import requests
from flask import g
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    response = requests.get("https://www.googleapis.com/oauth2/v3/tokeninfo"
                            "?id_token=" + token)

    if response.status_code != 200:
        return False

    data = response.json()
    if data['aud'] != '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54.apps' \
                      '.googleusercontent.com':
        return False

    g.user = {
        'google_id': data['sub'],
        'firstname': data['given_name'],
        'lastname': data['family_name'],
        'email': data['email']
    }

    return True
