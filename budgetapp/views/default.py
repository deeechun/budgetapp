from json import dumps as json
# convert dictionary to json
from plaid import Client
# The plaid API
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPNotFound

from pyramid.renderers import render_to_response

from pyramid.view import view_config
from pyramid.view import forbidden_view_config

from ..exceptions import EmailInvalidError
from ..exceptions import UsernameInvalidError
from ..models import BankAuth
from ..models import User
from ..utils import RegisterValidator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@view_config(route_name='accounts', renderer='../templates/accounts.jinja2',
			permission='view')
def accounts(request):
	"""
	View called when the '/accounts' route is called. Uses the plaid client to
	call the Accounts and Transactions endpoints in their API. This view is
	only callable when a user has a bank_auth associated with their user entry.

	"""
	user = request.user
	if user is None:
		next_url = request.route_url('login')
		return HTTPFound(next_url)

	# Create empty accounts and transactions lists
	accounts = []
	transactions = []

	# Query the database to get all bank_auths associated with the user and
	# loop through
	users_bank_auths = user.bank_auth.all()
	for bank_auth in users_bank_auths:

		# Get the access token associated with the bank auth to call the
		# Accounts API endpoint and append the response to the accounts list
		access_token = bank_auth.access_token
		account = _get_plaid_accounts(request, access_token)
		accounts.append(account)

		# Use the access token to access to Transactions API endpoint and
		# append the response to the transactions list
		transaction = _get_plaid_transactions(request, access_token)
		transactions.append(transaction)

	return {'accounts_list':accounts, 'transactions':transactions}




# ........................................................................... #
@view_config(route_name='add_bank',renderer='../templates/addbank.jinja2',
			permission='view')
def add_bank(request):
	"""
	View called when a GET request is called to the add_bank route. Renders the
	home template with no variables passed into it. This view is only called if
	the user is authenticated

	:param request: a GET request from an authenticated user to the add_bank
	route
	:type: pyramid.request.Request

	:return: dict
	"""
	return {}


# ........................................................................... #
@view_config(route_name='home', renderer='../templates/home.jinja2',
		request_method="GET")
def home(request):
	"""
	View called when a GET request is called to the home route. Renders the
	home template with no variables passed into it. Does not matter whether or
	not the user is authenticated or unauthenticated.

	:param request: a GET request to the home route
	:type: pyramid.request.Request

	:return: dict
	"""
	return {}

# ........................................................................... #
@view_config(route_name='register',
		renderer='../templates/register.jinja2', request_method="GET")
def register(request):
	"""
	View called when a GET request is called to the register route. Renders the
	register template with no variables passed into it

	:param request: an unauthenticated GET request to the register route
	:type: pyramid.request.Request

	:return: dict
	"""
	user = request.user
	if user != None:
		next_url = request.route_url('home')

	return {}


# ........................................................................... #
@view_config(route_name='register',
        renderer='../templates/register.jinja2', request_method = "POST")
def verify_register(request):
	"""
	View called when POST request is called to the register route. A validator
	class is created and supplies validation methods.

	:param request: a POST request to the 'register' route
	:type: pyramid.request.Request

	:return response: a redirect to the login route
	:rtype: pyramid.httpexceptions.HTTPFound
	"""

	# Grab request parameters from the form and set them to respective
	# namespaces
	username = request.params['username']
	email = request.params['email']
	password = request.params['password']
	confirm_password = request.params['confirm_password']

	# Create a RegisterValidator instance. The instance contains methods to
	# validate user credentials before adding them to users table. We pass in
	# the form parameters and the dbsession tied to the request into the
	# instance to validate internally.
	rv = RegisterValidator(username=username, email=email, password=password,
					confirm_password=confirm_password,
					dbsession=request.dbsession)

	try:
		# Checks to see if the username already exists in the table and throws
		# an error if it does
		username_exists = rv.check_username_exists()
	except UsernameInvalidError:
		# This error is raised if the username exists in the users table
		return {'error':'That username exists. Please choose a different one!'}

	# Call the User class method to create a user object with the parameters if
	# the registration checks pass
	user = User.create_user(username=username, email=email, password=password)
	request.dbsession.add(user)

	# Sets the URL to the '/login' route
	next_url = request.route_url('login')
	# Sets response to redirect to the '/login' route
	response = HTTPFound(next_url)
	#TODO: Finish register route
	return response


# ........................................................................... #
@view_config(route_name='set_access_token', request_method="POST")
def set_access_token(request):
	"""
	Sets access token in database and relates it to the logged in user. The
	access token is created through the exchange of our Plaid Link public token
	which we get from our request parameter. We use to access token to access
	API endpoints for the user that logged into the Plaid Link gateway for the
	specific bank chosen

	:param request: the POST HTTP request with an authorized cookie header.
	:type: pyramid.request.Request

	:return HTTPFound: A dict with the location of the next url
	:rtype: request.httpexceptions.HTTPFound
	"""

	# Gets request parameter that was returned from the frontend
	public_token = request.params['public_token']

	# Set client namespace to the plaid client used in the request
	client = request.plaid_client

	# Takes public token received from Plaid Link and exchanges it for an
	# access token. Access tokens are used to authenticate the usage of API
	# endpoints
	access_token = _get_access_token(request=request,
										public_token=public_token)

	# Ping Plaid's Item API endpoint with the newly exchanged access token to
	# get the institution name the access token is linked to
	item_response = client.Item.get(access_token)
	account_type_response = client.Institutions.get_by_id(item_response\
												['item']['institution_id'])
	account_type = account_type_response['institution']['name']

	# Get the authenticated user from the added request method 'user' and link
	# the BankAuth instance to the authenticated user, then add the BankAuth
	# into the db through the dbsession
	user = request.user
	# Create the BankAuth instance
	bankauth = BankAuth(access_token=access_token, account_type=account_type,
					user_id=user.id)

	request.dbsession.add(bankauth)

	# Sets the next url to the accounts route and redirects
	next_url = request.route_url('accounts')
	response = HTTPFound(next_url)
	return HTTPFound(next_url)


# ........................................................................... #
@forbidden_view_config(route_name='accounts', renderer='../templates/addbank.jinja2')
def forbidden_accounts(request):
	"""
	This view is called when permissions for a user do not meet the ACLs set in
	..routes for the accounts route. The logintemplate is rendered and prompts
	the user to add a bank account to their user account to view their accounts

	:param request: the request sent without proper ACLs to access the normal
	view
	:type: pyramid.request.Request

	:return response: the response sent back and renders the logintemplate
	:rtype: pyramid.response.Response
	"""
	# Sets the error message to send to jinja template
	error_msg = 'Add a bank to view your accounts!'

	# Render to response takes a template parameter, value parameters, and a
	# request parameter. Template parameter is the location of the template you
	# want to render in str format. Values is a dictionary with the variables
	# you want to send to the jinja template. The request parameter should be
	# set as the request parameter that pyramid sends when a view is called
	response = render_to_response('../templates/addbank.jinja2',
							{'error':error_msg}, request)
	return response


# ........................................................................... #
@forbidden_view_config(route_name='add_bank')
def forbidden_add_bank(request):
	"""
	This view is called when permissions for a user do not meet the ACLs set in
	..routes for the add_bank route. The logintemplate is rendered and prompts
	the user to log in to add a bank to their user account

	:param request: the request sent without proper ACLs to access the normal
	view
	:type: pyramid.request.Request

	:return response: the response sent back and renders the logintemplate
	:rtype: pyramid.response.Response
	"""
	# Sets the error message to send to jinja template
	error_msg = 'Please log in to add a bank!'

	# Render to response takes a template parameter, value parameters, and a
	# request parameter. Template parameter is the location of the template you
	# want to render in str format. Values is a dictionary with the variables
	# you want to send to the jinja template. The request parameter should be
	# set as the request parameter that pyramid sends when a view is called
	response = render_to_response('../templates/logintemplate.jinja2',
							{'error':error_msg}, request)
	return response


# ........................................................................... #
def _get_access_token(request, public_token):
	"""
	Gets the access token from the Plaid API by exchanging a public token
	delivered from the frontend through their Plaid Link front end software

	:param request: the request that is sent over from the frontend, containing
	the public token
	:type: pyramid.request.Request

	:param public_token: the public token that is returned from Plaid link
	:type: str

	:return access_token: the token exchanged for a valid public token
	:rtype: str
	"""
	# Send a request to the plaid API with the public token. Should return a
	# dictionary
	exchange_response = request.client.Item.public_token.exchange(public_token)

	# Access the dictionary's access_token value with the access_token key
	access_token = exchange_response['access_token']
	return access_token


# ........................................................................... #
def _get_plaid_accounts(request, access_token):
	"""
	Gets the bank account from the Plaid API. The specific bank account is
	linked to the unique access token.

	Example:
		- Chase bank will be linked to a certain access token
		- Wells Fargo bank will be linked to a different access token


	:param request: the request that is sent over from the frontend. We use it
	to access the Plaid client
	:type: pyramid.request.Request

	:param access_token: the access token that is linked to the specific
	bank account
	:type: str

	:return access_token: the token exchanged for a valid public token
	:rtype: str
	"""
	account = request.plaid_client.Accounts.get(access_token)
	return account


# ........................................................................... #
def _get_plaid_transactions(request, access_token):
	"""
	Gets transactions from the Plaid API. The specific bank account is
	linked to the unique access token.

	Example:
		- Chase bank will be linked to a certain access token
		- Wells Fargo bank will be linked to a different access token

	:param request: the request that is sent over from the frontend. We use it
	to access the Plaid client
	:type: pyramid.request.Request

	:param access_token: the access token that is linked to the specific
	bank account
	:type: str

	:return access_token: the token exchanged for a valid public token
	:rtype: str
	"""
	transaction = request.plaid_client.Transactions.get(access_token,
								start_date='2017-03-01', end_date='2017-03-31')
	return transaction
