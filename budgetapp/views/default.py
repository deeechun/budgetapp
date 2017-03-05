from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..utils.utils import auth_user_to_plaid
from ..utils.utils import get_access_token_from_auth_response
from ..models import MyModel


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'budgetapp'}

@view_config(route_name='login', renderer='../templates/logintemplate.jinja2',
		request_method="GET")
def login_view(request):
	return {}

@view_config(route_name='add_bank', renderer='../templates/addbanktemplate',
		request_method="GET")
def get_add_bank(request):
	account_type = request_method.matchdict['account_type']

@view_config(route_name='add_bank', request_method="POST")
def post_add_bank(request):
	username = request.params['username']
	password = request.params['password']
	


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
