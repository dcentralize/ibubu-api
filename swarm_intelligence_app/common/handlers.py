from flask import make_response
import json


def handle_entity_not_found(error):
    data = json.dumps({
        'success': False,
        'errors': [{
            'type': 'EntityNotFoundError',
            'reason': str(error)
        }]
    })
    status = 404
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(data, status, headers)


def handle_method_not_implemented(error):
    data = json.dumps({
        'success': False,
        'errors': [{
            'type': 'MethodNotImplementedError',
            'reason': str(error)
        }]
    })
    status = 405
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(data, status, headers)


def handle_entity_already_exists(error):
    data = json.dumps({
        'success': False,
        'errors': [{
            'type': 'EntityAlreadyExistsError',
            'reason': str(error)
        }]
    })
    status = 409
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(data, status, headers)
