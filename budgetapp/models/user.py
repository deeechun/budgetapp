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
	password = Column(Text)
	banking = relationship("AccessToken", uselist=False, back_populates="user")


# ............................................................................ #
class AccessToken(Base):

	__tablename__ = 'user_access_token'

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="banking")
