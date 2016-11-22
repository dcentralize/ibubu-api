from flask import make_response
import json


def handle_entity_not_found(error):
    data = json.dumps({
        'success': False,
        'errors': [{
            'type': 'EntityNotFoundError',
            'message': str(error)
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
            'message': str(error)
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
            'message': str(error)
        }]
    })
    status = 409
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(data, status, headers)


def handle_entity_not_modified(error):
    data = json.dumps({
        'success': False,
        'errors': [{
            'type': 'EntityNotModifiedError',
            'message': str(error)
        }]
    })
    status = 409
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(data, status, headers)
