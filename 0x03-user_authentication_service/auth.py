#!/usr/bin/env python3
"""
hashing password using bcrypt
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments
    and returns bytes.
    """
    salt = bcrypt.gensalt()
    hashed_paswd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_paswd


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
