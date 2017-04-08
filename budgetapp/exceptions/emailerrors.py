from .error import Error


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class EmailInvalidError(Error):

    def __init__(self):
        self.message = 'This email is invalid'

    def __str__(self):
        return str(self.message)
