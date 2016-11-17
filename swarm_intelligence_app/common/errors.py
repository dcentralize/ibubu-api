class EntityNotFoundError(Exception):
    def __init__(self, type, id):
        self.type = type
        self.id = id

    def __str__(self):
        return 'The {type} with id {id} does not exist'.format(
            type=self.type,
            id=self.id
        )


class EntityAlreadyExistsError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or 'The specified entity already exists.'


class MethodNotImplementedError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or 'The method you requested is not implemented ' \
                               'right now.'
