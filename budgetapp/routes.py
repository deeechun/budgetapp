from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Deny
from pyramid.security import Everyone

from .models import User


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('set_access_token', '/set_access_token')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('accounts', '/accounts', factory = account_factory)
    config.add_route('add_bank', '/add-bank', factory=add_bank_factory)


# ........................................................................... #
def add_bank_factory(request):
    add_bank = AddBank()
    return add_bank


# ........................................................................... #
class AddBank():
    """
    AddBank class created to set ACLs to give different permissions. Permission
    is denied if the user is not authenticated
    """

    def __acl__(self):
        permissions = [(Allow, Authenticated, 'view')]
        return permissions



# ........................................................................... #
def account_factory(request):
    user_has_bank_auth = check_for_bank_auth(request)
    return Account(request=request, user_has_bank_auth=user_has_bank_auth)


# ........................................................................... #
class Account():
    """
    Account created class to set ACLs to give different permissions. Permission
    is denied if the user does not have a bank account linked to their user
    account
    """

    # ....................................................................... #
    def __init__(self, request, user_has_bank_auth):
        """
        Instantiate this class with these parameters

        :param request: the request that we use to access the user
        :type: pyramid.request.Request

        :param user_has_bank_auth: checks to see if a user has linked a bank
        account to their user account
        :type: bool
        """
        self.request = request
        self.user_has_bank_auth = user_has_bank_auth

    def __acl__(self):

        if self.user_has_bank_auth:
            permissions = [(Allow, str(self.request.user.id), 'view')]
        else:
            permissions = [(Deny, Everyone, 'view')]

        return permissions


# ........................................................................... #
def check_for_bank_auth(request):
    user = request.user
    user_has_bank_auth = False
    if user is None:
        user_has_bank_auth = False
    else:
        user_bank_auths = user.bank_auth.all()
        if len(user_bank_auths) > 0:
            user_has_bank_auth = True
        else:
            user_has_bank_auth = False

    return user_has_bank_auth
