#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = os.getenv("AUTH_TYPE")

if auth_type == "auth":
    auth = Auth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    auth = SessionExpAuth()
else:
    # Default to BasicAuth if AUTH_TYPE is not specified or invalid
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorised(error) -> str:
    """
    unauthorised acceess error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    forbidden access error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    function to filter users
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)
    if auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
