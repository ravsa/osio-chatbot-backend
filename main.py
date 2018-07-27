#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to run the chatbot."""
from bot import run, train

T = train.Training()
T.train_nlu()
T.train_dialogue()

run.run()
