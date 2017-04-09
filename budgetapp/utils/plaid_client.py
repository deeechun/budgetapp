from plaid import Client
# Import Client to create client to communicate with Plaid

def get_plaid_client_from_settings(settings, prefix = 'plaid.'):
    plaid_client = Client(public_key=settings['plaid.public_key'],
                    client_id=settings['plaid.client_id'],
                    secret=settings['plaid.secret'],
                    environment=settings['plaid.environment'])
    return plaid_client


