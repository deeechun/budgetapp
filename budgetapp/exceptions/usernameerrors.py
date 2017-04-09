from .error import Error


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class UsernameInvalidError(Error):

    def __init__(self):
        self.message = 'This username is invalid'

    def __str__(self):
        return str(self.message)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
class UsernameExistsError(Error):

    def __init__(self):
        self.message = 'This username already exists'

    def __str__(self):
        return str(self.message)
