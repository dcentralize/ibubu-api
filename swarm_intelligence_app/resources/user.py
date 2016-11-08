from flask_restful import Resource, reqparse
from swarm_intelligence_app.models.models import db
from swarm_intelligence_app.models.user import User as UserModel
from swarm_intelligence_app.common import errors

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('firstname', required=True)
parser.add_argument('lastname', required=True)
parser.add_argument('email', required=True)

class UserList(Resource):
	def post(self):
		args = parser.parse_args()
		user = UserModel(
			args['firstname'],
			args['lastname'],
			args['email']
		)
		db.session.add(user)
		db.session.commit()
		return {'users': 'create'}

	def get(self):
		users = UserModel.query.all()
		list = [i.serialize for i in users]
		return {'users': list}

class User(Resource):
	def get(self, user_id):
		user = UserModel.query.get(user_id)
		if user == None:
			raise errors.EntityNotFoundError('User', user_id)
		return {'users': [user.serialize]}

	def put(self, user_id):
		args = parser.parse_args()
		user = UserModel.query.get(user_id)
		if user == None:
			raise errors.EntityNotFoundError('User', user_id)
		user.firstname = args['firstname']
		user.lastname = args['lastname']
		user.email = args['email']
		db.session.commit()
		return {'users': 'update'}

	def delete(self, user_id):
		user = UserModel.query.get(user_id)
		if user == None:
			raise errors.EntityNotFoundError('User', user_id)
		db.session.delete(user)
		db.session.commit()
		return {'users': 'delete'}