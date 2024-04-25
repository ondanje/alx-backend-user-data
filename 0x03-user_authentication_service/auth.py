#!/usr/bin/env python3
"""
hashing password using bcrypt
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments
    and returns bytes.
    """
    salt = bcrypt.gensalt()
    hashed_paswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_paswd


def _generate_uuid() -> str:
    """
    should return a string representation of a new UUID
    """
    myuuid = str(uuid.uuid4())

    return myuuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        initialize a new DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register  new users and return the user
        """
        try:
            user = self._db.find_user_by(email=email)

            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        valid_login method. It should expect email and password
        required arguments and return a boolean. to validate Credentials
        """
        try:
            user = self._db.find_user_by(email=email)

            if user:
                return bcrypt.checkpw(
                    password.encode("utf-8"), user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        method that takes an email string argument and
        returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)

            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        method to obtain the user using the session id
        """
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id=session_id)
        if not user:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        method to destroy the session depending on the  user id
        """
        try:
            user = self._db.find_user_by(user_id=user_id)
            user.session_id = None
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        get_reset_password_token method. It take an email string
        argument and returns a string.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError

        reset_token = _generate_uuid()

        user['reset_token'] = reset_token

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password method. It takes reset_token string
        argument and a password string argument and returns None
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError

        hash_password = _hash_password(password)

        self._db.update_user(user.id, hash_password=hash_password)
        self._db.update_user(user.id, reset_token=None)
