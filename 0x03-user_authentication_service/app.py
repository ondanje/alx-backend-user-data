#!/usr/bin/env python3
"""
Basic flask app setup
"""
from flask import Flask, abort, jsonify, make_response, redirect, request
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index() -> str:
    """
    return a simple message
    """
    form = {"message": "Bienvenue"}
    return jsonify(form)


@app.route('/users', methods=["POST"])
def create_new_user():
    """
    If the user does not exist, the end-point should
    register it and respond with the following JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    login method to handle logging in
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, "Email and Password are required")

    user = AUTH.valid_login(email, password)

    if not user:
        abort(401)

    session_id = AUTH.create_session(email)
    res = make_response(jsonify({"email": f"{email}", "message": "logged in"}))
    res.set_cookie("session_id", session_id)

    return res


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    method to implement logging out
    """
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        abort(403)
    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    method to display a profile view
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403, "DENIED")

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
