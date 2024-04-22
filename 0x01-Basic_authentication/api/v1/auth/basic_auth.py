#!/usr/bin/env python3
"""
Basic auth class to manage authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from flask import request
from typing import List, TypeVar

from models.user import User


class BasicAuth(Auth):
    """
    a class BasicAuth that inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication:
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        method to return the  returns the decoded
        value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):  # type: ignore
        """
        method that returns the user email
        and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return(None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        colon_index = decoded_base64_authorization_header.find(':')
        if colon_index < 0:
            return (None, None)

        user_email = decoded_base64_authorization_header[:colon_index]
        user_pwd = decoded_base64_authorization_header[colon_index + 1:]

        return (user_email, user_pwd)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):  # type: ignore
        """
        method that returns the User instance
        based on his email and password.
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        method that overloads Auth and retrieves the User
        instance for a request:
        """
        auth_header = self.authorization_header(request)
        extracted_header = self.extract_base64_authorization_header(
            auth_header
            )
        decoded_header = self.decode_base64_authorization_header(
            extracted_header
            )
        email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, password)
