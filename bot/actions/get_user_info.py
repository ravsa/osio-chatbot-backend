#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get user information actions."""

from rasa_core.actions import Action
from rasa_core.events import SlotSet
from server.auth import decode_token


class MyProfile:
    """User-Information."""

    def __init__(self):
        """Initialize with defaults."""
        self.name = None
        self.email = None
        self.handler = None
        try:
            decoded_token = decode_token()
            self.name = decoded_token.get('given_name')
            self.email = decoded_token.get('email')
            self.handler = decoded_token.get('preferred_username')
        except Exception as exe:
            print(exe)


class GetUserInfoAction(Action):
    """User info action class."""

    def name(self):
        """Getuserinfoaction class identity."""
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        """Run method to execute action."""
        my_profile = MyProfile()
        return [SlotSet("user_name", my_profile.name if my_profile.name else ''),
                SlotSet("email", my_profile.email if my_profile.name else ''),
                SlotSet("handler", my_profile.handler if my_profile.name else '')]
