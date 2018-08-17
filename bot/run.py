#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run chatbot."""
import os
import logging
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from .train import Training

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Bot(Training):
    """Main Bot class to run bot."""

    def __init__(self):
        """Initialize the Bot class."""
        super().__init__()

    def console_run(self, serve_forever=True):
        """Run the Console server.

        serve_forever: Boolean
        """
        interpreter = RasaNLUInterpreter(os.path.join(
            self.base_path, "models/nlu/default/", self._model_name))
        agent = Agent.load(os.path.join(self.base_path,
                                        "models/dialogue"), interpreter=interpreter)

        if serve_forever:
            agent.handle_channel(ConsoleInputChannel())
        return agent

    def run(self, text_message, message_preprocessor=None, message_postprocessor=None,
            output_channel=None, sender_id='default'):
        """Parse the user_input and return the list of responses."""
        print("USER SAID: ", text_message)
        interpreter = RasaNLUInterpreter(os.path.join(
            self.base_path, "models/nlu/default/", self._model_name))
        agent = Agent.load(os.path.join(self.base_path,
                                        "models/dialogue"), interpreter=interpreter)
        output = agent.handle_message(text_message, message_preprocessor,
                                      output_channel, sender_id)
        if message_postprocessor is not None:
            return message_postprocessor(output)
        return agent.handle_message(text_message, message_preprocessor, output_channel, sender_id)

    def run_nlu(self):
        """Parse the user_input and return the list of responses."""
        interpreter = RasaNLUInterpreter(os.path.join(
            self.base_path, "models/nlu/default/", self._model_name))
        while True:
            __import__('pprint').pprint(interpreter.parse(input("Type> ")))

    def train(self):
        """Train the NLU and Dialogue model."""
        self.train_nlu()
        self.train_dialogue()
