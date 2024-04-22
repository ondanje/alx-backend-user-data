#!/usr/bin/env python3
"""
module to creates a route for session authentication
"""
from api.v1 import auth
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'])
def session_login():
    """
    implementing login session
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    user = User.search(email=email)
    if user is None:
        return jsonify({'error': 'no user found for this email'}), 404

    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(auth.SESSION_NAME, session_id)
    return response
