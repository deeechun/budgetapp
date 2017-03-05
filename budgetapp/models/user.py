import bcrypt

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .meta import Base

class User(Base):

	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	username = Column(Text, nullable = False)
	email = Column(Text, nullable = False)
	_hashed_password = Column(Text)
	banking = relationship("AccessToken", uselist=False, back_populates="user")

	def __init__(self, password):
		"""
		Creates the '_hashed_password' parameter by calling on the method
		'set_hashed_password' upon instance initialization
		"""
		self._hashed_password = set_hashed_password(password)

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

	def check_password_hash(self, password):
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

# ............................................................................ #
class AccessToken(Base):

	__tablename__ = 'user_access_token'

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="banking")
