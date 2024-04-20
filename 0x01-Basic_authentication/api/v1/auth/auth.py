#!/usr/bin/env python3
"""
Auth class to manage authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        public method def require_auth(self, path: str,
        excluded_paths: List[str]) -> bool: that returns
        False - path and excluded_paths for now
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        def authorization_header(self, request=None)
        -> str: that returns None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        Get the current user based on the request.
        Returns None for now, will be updated later.
        """
        return None
