#!/usr/bin/env python3
"""
Module to create Session Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
     a class SessionAuth that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session id for a user
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Method that returns a User ID based on a session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a user instance based on a cookie value

        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        try:
            return User.get(user_id)
        except Exception as e:
            raise Exception(f"Error retrieving user id: {e}")
