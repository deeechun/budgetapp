from ..exceptions import EmailExistsError
from ..exceptions import UsernameExistsError

from ..models import User


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class RegisterValidator():
    """
    Class created to check for new register validity. Functions are checks on
    username, email, and confirmed passwords
    """

    # ....................................................................... #
    def __init__(self, request):
        """
        Parameters of the class. Username, email, password, and
        confirm_password are parameters from the request object, and the
        dbsession should also be provided from the request.

        :param username: the username passed in from a form page in the
        username field
        :type: str

        :param email: the email passed in from a form page in the email field
        :type: str

        :param password: the password passed in from a form page in the
        password field
        :type: str

        :param confirm_password: the confirm password passed in from a form
        page in the confirm password field
        :type: str
        """
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.dbsession = dbsession


    # ....................................................................... #
    def check_username_exists(self):
        """
        Checks to see if username exists in the database. First does a check to
        see if '@' char is in the username and raises an error if it present.
        Then queries the database with the username. Returns True if the
        username is in the db and False if not

        :return username_exists: whether or not the username exists in the
        users table in the username column

        :raises UsernameInvalidError: if '@' is found in the username
        :raises UsernameExistsError: if username exists in users table
        """
        if '@' in self.username:
            raise UsernameInvalidError()
        else:
            username_exists = User.check_username_exists(self.username,
                                                self.dbsession)
        return username_exists


    # ....................................................................... #
    def check_email_exists(self):
        """
        Checks to see if email exists in the database. Checks to make sure that
        '@' is in the email and raises an error if it doesn't. Then queries the
        table with the email. Returns True if the email is in the db and False
        if not

        :return email_exists: whether or not the email exists in the
        users table in the email column
        :rtype: bool

        :raises EmailExistsError:
        """
        if '@' not in self.email:
            raise EmailInvalidError()
        else:
            email_exists = User.check_username_exists(self.username,
                                                self.dbsession)
        return email_exists

    # ....................................................................... #
    def check_passwords_match(self):
        """
        Checks to see that the password and confirm_password attributes are of
        the exact same value

        :return passwords_match: whether or not the password and
        confirm_password attributes are the same value
        :rtype: bool
        """
        # Compare value of password and confirm_password attributes
        if self.password == self.confirm_password:
            passwords_match = True
        else:
            passwords_match = False
        return passwords_match


    # ....................................................................... #
