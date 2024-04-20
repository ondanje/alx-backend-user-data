#!/usr/bin/env python3
"""
Basic auth class to manage authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from flask import request
from typing import List, TypeVar


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
