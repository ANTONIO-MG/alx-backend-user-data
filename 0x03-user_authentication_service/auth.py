#!/usr/bin/env python3
"""
a pthon module that executes authentications
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    method that takes a password and returns a password in bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        initiates all the elements under thius classs at the object creation
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> object:
        """
        a public method that registers a user tot he database
        """
        new_user = self._db._session.query(User).filter_by(email=email).first()
        if new_user:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
