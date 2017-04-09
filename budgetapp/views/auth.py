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
	View for the login page. Function called when route URL is matched.
	"""
	# This 'form.submitted' will be in request parameters if the submit button
	# is clicked. This then redirects to the same route and calls the
	# verify_login_view
	if 'form.submitted' in request.params:
		next_url = request.route_url('login')
		return HTTPFound(next_url)
	return {}


# ............................................................................ #
@view_config(route_name='login', request_method="POST")
def verify_login_view(request):
	username = request.params['username']
	password = request.params['password']
	user = request.dbsession.query(User).filter_by(username=username).first()

	# Check to see if username is present in db and password matches with one
	# stored in db
	if user != None and user.check_password(password):
		# Checks to see if the password matches the stored password in db
		next_url = request.route_url('accounts')
		headers = remember(request, user.id)
		return HTTPFound(location = next_url, headers = headers)



# ............................................................................ #
@view_config(route_name='logout')
def logout_view(request):
	headers = forget(request)
	next_url = request.route_url('login')
	print("########################")
	print(next_url)
	print("########################")
	return HTTPFound(location=next_url, headers=headers)
