from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from ..utils.utils import auth_user_to_plaid
from ..utils.utils import get_access_token_from_auth_response
from ..models import BankAuth
from ..models import User

# ............................................................................ #
@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'budgetapp'}


# ............................................................................ #
@view_config(route_name='login', renderer='../templates/logintemplate.jinja2',
		request_method="GET")
def login_view(request):
	"""
	View for the login page. Function called when route URL is matched. 
	"""
	# This 'form.submitted' will be in request parameters if the submit button
	# is clicked. This then redirects to the same route and calls the
	# verify_login_view
	if 'form.submitted' in request.params:
		next_url = request.route_url('verify_login')
		return HTTPFound(next_url)
	return {}


# ............................................................................ #
@view_config(route_name='login',renderer='../templates/logintemplate.jinja2',
		request_method="POST")
def verify_login_view(request):
	username = request.params['username']
	password = request.params['password']
	user = request.dbsession.query(User).filter_by(username=username).first()
	
	# Check to see if username is present in db and password matches with one
	# stored in db
	if user != None and user.check_password(password):
		# Checks to see if the password matches the stored password in db
		next_url = request.route_url('home')
		return HTTPFound(next_url)
	else:
		return Response("""###############################################""")

# ............................................................................ #
@view_config(route_name='create_account',
		renderer='../templates/createaccounttemplate.jinja2',
		request_method="GET")
def create_account_view(request):
	return {}


# ............................................................................ #
@view_config(route_name='add_bank', renderer='../templates/addbanktemplate',
		request_method="GET")
def add_bank_view(request):
	account_type = request_method.matchdict['account_type']



# ............................................................................ #
@view_config(route_name='add_bank', request_method="POST")
def verify_add_bank_view(request):
	username = request.params['username']
	password = request.params['password']


# ............................................................................ #
db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_budgetapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
