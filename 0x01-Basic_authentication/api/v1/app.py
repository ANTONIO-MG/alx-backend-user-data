#!/usr/bin/env python3
"""
Route module for the API
This module handles the routing for the API.
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
import os


"""
The app variable is an instance of the Flask class.
It is used to create the API.
"""

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Determine AUTH_TYPE from environment variable
auth_type = getenv('AUTH_TYPE')

if auth_type == 'auth':
    auth = Auth()


@app.before_request
def before_request_func():
    """
    Handler for before each request
    This function is called before each request and checks for authentication.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles the NotFound error
    This function returns a JSON response with a 404 status code.
    """
    return jsonify({"error": "Unauthorized"}), 404


@app.errorhandler(401)
def no_access(error) -> str:
    """
    Handles the Unauthorized error
    This function returns a JSON response with a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def no_allowed(error) -> str:
    """
    Handles the Forbidden error
    This function returns a JSON response with a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    """
    This executes the code when its on teh main and not when exported.
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
