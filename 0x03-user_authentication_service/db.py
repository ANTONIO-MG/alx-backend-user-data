#!/usr/bin/env python3
"""
Database module, that connects the data to the database
"""
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """
    Database class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, mail: str, password: str) -> object:
        """
        Method that creates a user and returns a user object
        """
        new_user = User(email=mail, hashed_password=password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs: str) -> object:
        """
        This method takes in arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the methods input arguments
        """
        answer = None
        try:
            answer = self._session.query(User).filter_by(**kwargs).first()
            if answer is None:
                for key in kwargs:
                    if key == 'email':
                        raise sqlalchemy.orm.exc.NoResultFound
                    else:
                        raise sqlalchemy.exc.InvalidRequestError
            return answer
        except sqlalchemy.orm.exc.NoResultFound:
            raise
        except sqlalchemy.exc.InvalidRequestError:
            raise
        except Exception as e:
            raise e

    def update_user(self, id: int, **kwargs: str) -> None:
        """
        a method that updates a user and returns non
        or raises a ValueError if user not found.
        """
        try:
            user_to_update = self.find_user_by(id=id)
            if user_to_update is None:
                raise ValueError
            else:
                if user_to_update.id == id:
                    for key, value in kwargs.items():
                        setattr(user_to_update, key, value)
                self._session.commit()
                return None
        except ValueError as e:
            raise e
