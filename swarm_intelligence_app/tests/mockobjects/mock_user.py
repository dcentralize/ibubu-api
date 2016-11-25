class MockUser:
    token = ''

    def __init__(self, token):
        self.token = token

    def get_token(self):
        return self.token