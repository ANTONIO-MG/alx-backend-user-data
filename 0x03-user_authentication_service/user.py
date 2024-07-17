#!/usr/bin/env python3
"""
Class fro  creating a base model for a User
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    Creates a user object and maps it to the databse using sqlalchemy
    Returns:
        - returns a user object
    """
    # the name of the table in hte database
    __tablename__ = 'users'

    # the columns and fields of the table
    id = Column(Integer, primary_key=True)  # the integer primary key
    email = Column(String(250), nullable=False)  # a non-nullable string
    hashed_password = Column(String(250), nullable=False)  # a non-nullable
    session_id = Column(String(250))  # a nullable string
    reset_token = Column(String(250))  # a nullable string

    def __rep__(self):
        """
        creates a database name representation of the user object
        Returns:
            - returns a string representation of the object
        """
        return f"<User(id='{self.id}', email='{self.email}')>"
