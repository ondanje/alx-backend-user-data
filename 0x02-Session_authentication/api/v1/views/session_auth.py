#!/usr/bin/env python3
"""
module to creates a route for session authentication
"""
from api.v1 import auth
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route("/auth_session/login", strict_slashes=False, methods=["POST"])
def session_authenticate():
    """
    Handles routes for session authentication
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email:
        return jsonify({'error': 'email missing'}), 400
    if not user_password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": user_email})
    if not user:
        return jsonify({"error": "no user found for this email"})
    if not user[0].is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(getattr(user[0], "id"))
    response = jsonify(user[0].to_json())
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'])
def logout():
    """
    implementing logout
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
