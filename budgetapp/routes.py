from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Deny
from pyramid.security import Everyone

from .models import User


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def includeme(config):
    # Add location of static assets
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Add in route names and their corresponding paths
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('set_access_token', '/set_access_token')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    # Add in a factory to customize ACLs
    config.add_route('accounts', '/accounts', factory=account_factory)
    config.add_route('add_bank', '/add-bank', factory=add_bank_factory)


# ........................................................................... #
def add_bank_factory(request):
    """
    Factory created to customize permissions for views affecting the add_bank
    route

    :param request: any request to the add_bank route. Only authenticated users
    are given permission
    :type: pyramid.request.Request

    :return add_bank: an instance of the AddBank class with an altered __acl__
    attribute
    :rtype: budgetapp.routes.AddBank
    """
    add_bank = AddBank()
    return add_bank


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
class AddBank():
    """
    AddBank class created to set ACLs to give different permissions. Permission
    is denied if the user is not authenticated
    """

    def __acl__(self):
        # Tie ACL to only allow authenticated users to have 'view' permissions
        # to this page
        permissions = [(Allow, Authenticated, 'view')]
        return permissions



# ........................................................................... #
def account_factory(request):
    """
    Factory created to customize permissions for views affecting the accounts
    route

    :param request: any request to the add_bank route. If an authenticated user
    has added a bank account to their user account, they are allowed to view
    the accounts page. Otherwise, everybody else is denied
    :type: pyramid.request.Request

    :return account: an instance of the Account class with an altered __acl__
    attribute
    :rtype: budgetapp.routes.Account
    """
    user_has_bank_auth = check_for_bank_auth(request)
    account = Account(request=request, user_has_bank_auth=user_has_bank_auth)
    return account


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
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
            # Tie ACL to the specific user id and give 'view' permissions
            permissions = [(Allow, str(self.request.user.id), 'view')]
        else:
            # Tie ACL to specific user and deny every user attempting to access
            # if the user doesn't have any bank accounts linked
            permissions = [(Deny, Everyone, 'view')]

        return permissions


# ........................................................................... #
def check_for_bank_auth(request):
    """
    Checks to see if a user has any bank_authorizations linked to their user
    account. Returns True if their is a bank account linked and False if not

    :param request: any request object used to pull the user tied to the
    request
    :type: pyramid.request.Request

    :return user_has_bank_auth: bool determining whether or not the user has a
    bank account linked
    :rtype: bool
    """
    # Get the authenticated user. Returns None if no user is authenticated
    user = request.user

    if user is None:
        # Set user_has_bank_auth to False if user is not authenticated
        user_has_bank_auth = False
    else:
        # Call if user is authenticated and query for all their linked
        # bank_authorizations. Returned as a list
        user_bank_auths = user.bank_auth.all()

        # Length of list will be greater than 0 if there are linked bank auths
        if len(user_bank_auths) > 0:
            user_has_bank_auth = True
        else:
            user_has_bank_auth = False

    return user_has_bank_auth
