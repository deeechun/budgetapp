from plaid import Client
from plaid.utils import json

def auth_user_to_plaid(client, account_type, username, password):
	client_response = client.auth(account_type, {'username':username, 'password':
										password})
	return client_response

def get_access_token_from_auth_response(auth_response):
	return response.json['access_token']

def get_auth_user_balance(client_id, secret, access_token):
	client = Client(client_id=client_id, secret=secret,
				access_token=access_token)
	client_response = client.balance()
	balance = client_response.json()
	return balance

def get_auth_user_transactions(client_id, secret, access_token):
	client = Client(client_id=client_id, secret=secret,
				access_token=access_token)
	client_response = client.connect_get()
	transactions = client_response.json()
	return transactions