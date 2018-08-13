#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for mattermost utility."""


from rasa_core.channels.channel import OutputChannel
from bot import Bot
from mattermostdriver import Driver
import asyncio
import json
import os


driver = Driver({
    'url': os.getenv('MATTERMOST_URL') or 'chat.openshift.io',
    'port': os.getenv('MATTERMOST_PORT') or 443,
    'login_id': os.getenv('MATTERMOST_LOGIN_ID'),
    'password': os.getenv('MATTERMOST_PASSWORD'),
    'debug': False
})


bot = Bot()


class MatterMostOutputChannel(OutputChannel):
    """Interact with the mattemost."""

    @classmethod
    def name(cls):
        """Every channel needs a name to identify it."""
        return "mattermost_output"

    def send_text_message(self, recipient_id, message):
        """Post message to user."""
        driver.posts.create_post({
            'channel_id': recipient_id,
            'message': message
        })


@asyncio.coroutine
def event_handler(message):
    """Logic to handle websocket events."""
    response = json.loads(message)
    if response.get('event') == 'posted':
        data = response.get('data', {})
        sender_name = data.get('sender_name', '')
        try:
            post = json.loads(data.get('post', {}))
            msg = post.get('message', '')
            channel_id = post.get('channel_id')
            # "bot" is mattermost user name
            if sender_name != 'bot':
                bot.run(text_message=msg,
                        output_channel=MatterMostOutputChannel(),
                        sender_id=channel_id)

        except json.JSONDecodeError:
            # ignore
            pass


def mattermost_runner():
    """Runner function for the mattermost."""
    driver.login()
    driver.init_websocket(event_handler)
