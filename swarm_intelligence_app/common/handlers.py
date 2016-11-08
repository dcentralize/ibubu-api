from flask import make_response
import json

def handle_entity_not_found(error=None):
	error = error or 'The entity you requested was not found.'
	data = json.dumps({
		'type': 'EntityNotFoundError',
		'reason': str(error)
	})
	status = 404
	headers = {
		'Content-Type': 'application/json'
	}
	return make_response(data, status, headers)