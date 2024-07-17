#!/usr/bin/env python3
"""
This module handles API authentication.
"""

from flask import request
from typing import TypeVar


class Auth():
    """ 
    Class that handles user authentication
    """
    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        """ takes a path and a list of excluded path
        Return:
            - A bool depending on the existance access granted
        """
        # step 1
        if path is None:
            return True
        # step 2
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # step 3
        if path[-1] != "/":
            path += "/"
        # step 4
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ 
        takes request object and checks if it is ! None.
        Return:
            - the value of the header request Authorization or None
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ 
        takes request object and checks if it is ! None.
        Return:
            - request or None
        """
        if request is not None:
            return request
        else:
            return None
