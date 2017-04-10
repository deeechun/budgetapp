from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import forget
from pyramid.security import remember

from ..models import User


@view_config(route_name='login', renderer='../templates/logintemplate.jinja2',
		request_method="GET")
def get_login_view(request):
	"""
	View for the login page. Function called when GET HTTP request is is called
	to the home route.
	"""
	return {}


# ............................................................................ #
@view_config(route_name='login', request_method="POST")
def verify_login_view(request):
	"""
	View called when POST request is called to the login route. If the username
	exists in the users table, check the password stored in the table against
	the provided password in the request parameters

	:param request: a POST request to the 'login' route
	:type: pyramid.request.Request

	:return response: a redirect to the account route
	:rtype: pyramid.httpexceptions.HTTPFound
	"""
	# Store request parameters into respective namespaces
	username = request.params['username']
	password = request.params['password']
	# Query database for the username
	user = request.dbsession.query(User).filter_by(username=username).first()

	# Check first to see if username is present in db then whether or not the
	# password matches with one stored in table
	if user != None and user.check_password(password):
		# Checks to see if the password matches the stored password in db
		next_url = request.route_url('accounts')
		# Create 'Set-Cookie' headers, stored with the newly authenticated
		# user's id
		headers = remember(request, user.id)
		return HTTPFound(location = next_url, headers = headers)



# ............................................................................ #
@view_config(route_name='logout', request_method="POST")
def logout_view(request):
	"""
	View called when POST request is called to the logout route. This logs a
	user out by sending a Set-Cookie header with a blank sequence, overwriting
	any previous cookies set. If the request sent is not authenticated, the
	user will stil be logged out and redirected to the login route

	:param request: the POST request sent to the server to unauthenticate a
	user
	:type: pyramid.request.Request

	:return HTTPFound: redirects to the login route after unauthenticating the
	user
	:rtype: pyramid.httpexceptions.HTTPFound
	"""
	headers = forget(request)
	next_url = request.route_url('login')
	return HTTPFound(location=next_url, headers=headers)
