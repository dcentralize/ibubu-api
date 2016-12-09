"""
Define any error classes for the application.

"""


class EntityNotFoundError(Exception):
    """
    Define an EntityNotFoundError.

    """
    def __init__(self, type, id):
        """
        Initialize an EntityNotFoundError.

        """
        self.type = type
        self.id = id

    def __str__(self):
        """
        Return an EntityNotFoundError as a readable message.

        """
        return 'The {type} with id {id} does not exist'.format(
            type=self.type,
            id=self.id
        )


class MethodNotImplementedError(Exception):
    """
    Define an MethodNotImplementedError.

    """
    def __init__(self,
                 message=None):
        """
        Initialize an MethodNotImplementedError.

        """
        self.message = message

    def __str__(self):
        """
        Return an MethodNotImplementedError as a readable message.

        """
        return self.message or 'The method you requested is not implemented ' \
                               'right now.'


class EntityAlreadyExistsError(Exception):
    """
    Define an EntityAlreadyExistsError.

    """
    def __init__(self,
                 message=None):
        """
        Initialize an EntityAlreadyExistsError.

        """
        self.message = message

    def __str__(self):
        """
        Return an EntityAlreadyExistsError as a readable message.

        """
        return self.message or 'The specified entity already exists.'


class EntityNotModifiedError(Exception):
    """
    Define an EntityNotModifiedError.

    """
    def __init__(self,
                 message=None):
        """
        Initialize an EntityNotModifiedError.

        """
        self.message = message

    def __str__(self):
        """
        Return an EntityNotModifiedError as a readable message.

        """
        return self.message or 'The specified entity cannot be modified.'
