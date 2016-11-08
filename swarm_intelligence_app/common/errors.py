class EntityNotFoundError(Exception):
	def __init__(self, type, id):
		self.type = type
		self.id = id

	def __str__(self):
		return '{type} with id {id} does not exist'.format(
			type=self.type,
			id=self.id
		)