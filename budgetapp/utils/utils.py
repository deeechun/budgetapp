from plaid import Client
from plaid.utils import json

def auth_user_to_plaid(client, account_type, username, password):
	client_response = client.auth(account_type, {'username':username, 'password':
										password})
	return client_response

def get_access_token_from_auth_response(auth_response):
	return response.json['access_token']

