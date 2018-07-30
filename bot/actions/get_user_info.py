#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get user information actions."""

from rasa_core.actions import Action
from rasa_core.events import SlotSet


class MyProfile:
    """User-Information."""

    def __init__(self):
        """Initialize with defaults."""
        self.name = None
        self.token = None
        self.email = None


class GetUserInfoAction(Action):
    """User info action class."""

    def name(self):
        """Getuserinfoaction class identity."""
        return "action_userinfo"

    def run(self, dispatcher, tracker, domain):
        """Run method to execute action."""
        return [SlotSet("user_name", '')]
