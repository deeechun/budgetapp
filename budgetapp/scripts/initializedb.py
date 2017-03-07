import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import BankAuth
from ..models import User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        # Create sample entry and add to users table
        username = "admin"
        email = "dechun92@gmail.com"
        password = "password"
        user = User(username=username, email=email, password=password)

        # Create sample entry and add to access_token table
        access_token = "463505f3cf167e96c6ca808f1922a234f9de0898a4c82301cad9" /
        +"ccd13f18f7c0440b7a90a6834cba4296acf758913dd5228f05f546b93ed44f0df3" /
        +"a4dbf703e8cee266efe781e34f92c33d353e4bd530"
        account_type = "chase"
        bank_auth = BankAuth(access_token=access_token,
                        account_type=account_type)

        dbsession.add_all([user, bank_auth])
        