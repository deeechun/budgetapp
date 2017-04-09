import bcrypt

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .meta import Base

class User(Base):

	# Sets db table name
	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	username = Column(Text, nullable = False)
	email = Column(Text, nullable = False)
	_hashed_password = Column('password', Text)
	bank_auth = relationship("BankAuth", backref="user", lazy='dynamic')


	# ....................................................................... #
	def __init__(self, password, username, email):
		"""
		Creates the '_hashed_password' parameter by calling on the method
		'set_hashed_password' upon instance initialization
		"""
		self._hashed_password = self.set_hashed_password(password)
		self.username = username
		self.email = email


	# ....................................................................... #
	@classmethod
	def check_username_exists(cls, username, dbsession):
		"""
		Checks to see if username exists in the database table

		:param username: username to query the database
		:type: str

		:param dbsession: the session with the database
		:type: pyramid.request.Request.dbsession

		:return username_exists: a bool depending on whether or not the
		username exists
		:rtype: bool
		"""
		# Query the User table for the username
		username_in_db = dbsession.query(User).filter_by(username=username).\
								first()
		# Sets username_exists to False
		username_exists = False

		# Change username_exists value if username_exists is not None
		if username_in_db:
			username_exists = True
		return username_exists


    # ....................................................................... #
	@classmethod
	def create_user(cls, username, email, password):
	    """
	    Returns the created User object with given username, email, password.
	    The password is hashed for security using bcrypt. The role for the
	    returned User is set to 'user'.

	    :param username: the name the user wants to be addressed as
	    :type username: str

	    :param email: the user's email address. We filter the emails and must
	    have an '@' in it to be added in as a column
	    :type email: str

	    :param password: the password the user wants to set for the account
	    :type password: str

	    :param role: the role of the user. We will be using this in our set
	    authorization policy
	    :type role: str

	    :return: created User instance
	    :rtype: skrus.models.user.User
	    """

	    # get the hash the password
	    hashed_password = cls._get_hash_password(password)

	    # create a user with given username, email, hashed password and role
	    # set to 'role'
	    return User(username=username,
	                email=email,
	                _hashed_password=hashed_password,
	                role='user')


	# ....................................................................... #
	@classmethod
	def get_username_by_username_or_email(username, dbsession):
		pass


	# ....................................................................... #
	def set_hashed_password(self, password):
		"""
		Sets a password hash after encrypting the password argument. This
		will throw a TypeError if the 'str' method cannot be applied to the
		password parameter

		:param password: the password a user wants to set as his/her own
	:type str: preferably a string, but 'str' method will be applied to the
		parameter
		"""
		password_string = str(password)
		hashed_password = bcrypt.hashpw(password_string.encode('utf8'),
									bcrypt.gensalt())
		self._hashed_password = hashed_password.decode('utf8')
		return self._hashed_password


	# ....................................................................... #
	def check_password(self, password):
		"""
		Checks against the set password hash and verify it matches. If there is
		no password hash set for the instance, there will be no verification
		and False will be returned. If the 'str' method cannot be applied to
		the provided parameter, a TypeError will be raised

		:param password: The password you want to match against the stored hash
		:type str: preferably a string, but the 'str' method will be applied to
		the parameter

		:return password_matches:
		:rtype bool:
		"""
		password_matches = False
		stored_hash = self._hashed_password
		password_string = str(password)
		if stored_hash != None:
			encoded_stored_hash = self._hashed_password.encode('utf8')
			password_matches = bcrypt.checkpw(password_string.encode('utf8'),
										encoded_stored_hash)
		return password_matches


# ........................................................................... #
class BankAuth(Base):

	# Sets db table name
	__tablename__ = 'bank_auth'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	_access_token = Column(Text, nullable = False)
	account_type = Column(Text, nullable = False)

	def __init__(self, access_token, account_type, user_id):
		self._access_token = access_token
		self.account_type = account_type
		self.user_id = user_id

	@property
	def access_token(self):
		return self._access_token
