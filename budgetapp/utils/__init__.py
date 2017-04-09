from .plaid_client import get_plaid_client_from_settings
from .registerer import RegisterValidator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def includeme(config):

    # Returns settings found in the .ini file specified when running pserve
    settings = config.get_settings()

    # Create the client used to communicate with API
    plaid_client = get_plaid_client_from_settings(settings)

    # Adds as a request method to make it accessible through the request
    config.add_request_method(lambda r:
                        get_plaid_client_from_settings(settings),
                        'plaid_client',
                        reify=True)
