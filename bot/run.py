#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from .train import Training


training_obj = Training()


def train():
    training_obj.train_nlu()
    training_obj.train_dialogue()


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter(os.path.join(
        training_obj.base_path, "models/nlu/default/", training_obj._model_name))
    agent = Agent.load(os.path.join(training_obj.base_path,
                                    "models/dialogue"), interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


train()
run()
