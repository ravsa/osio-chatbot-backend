#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for training models."""

import yaml
import glob
import tempfile
import os
from rasa_nlu.training_data import load_data
from rasa_core.agent import Agent
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_core.policies.memoization import MemoizationPolicy
from .policies.chatbot_policy import ChatBotPolicy


class Training:
    """Training class for NLU and Dialogue training."""

    _model_name = 'chatbot-001'

    def __init__(self,
                 domains_directory="actions/domains",
                 dialogue_model_path="models/dialogue",
                 nlu_model_path='models/nlu',
                 dialogue_training_data_dir='actions/dialogue_training_stories',
                 nlu_training_data='data/nlu_training_data.json',
                 nlu_model_config_file='configs/nlu_config.yml'):
        """Initialize the Training class object."""
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.domains_directory = os.path.join(
            self.base_path, domains_directory)
        self.dialogue_model_path = os.path.join(
            self.base_path, dialogue_model_path)
        self.nlu_model_path = os.path.join(self.base_path, nlu_model_path)
        self.dialogue_training_data_dir = os.path.join(
            self.base_path, dialogue_training_data_dir)
        self.nlu_training_data = os.path.join(
            self.base_path, nlu_training_data)
        self.nlu_model_config_file = os.path.join(
            self.base_path, nlu_model_config_file)

    def get_domain_file(self):
        """Combine the all domain yaml files and return as single."""
        data = {
            'slots': dict(),
            'entities': set(),
            'intents': set(),
            'templates': dict(),
            'actions':  set()
        }
        filepath = tempfile.NamedTemporaryFile(
            prefix='domain-', suffix='.yml', delete=False).name
        with open(filepath, 'w') as file:
            for yml_file in glob.glob(os.path.join(self.domains_directory, '*.yml')) +\
                    glob.glob(os.path.join(self.domains_directory, '*.yaml')):
                yaml_data = yaml.load(open(yml_file))
                if yaml_data:
                    for k, v in yaml_data.items():
                        data[k].update(v)
            for k, v in data.items():
                if isinstance(v, set):
                    data[k] = list(v)
                else:
                    data[k].update(v)
            yaml.dump(dict(data), file, default_flow_style=False)
        return filepath

    def train_nlu(self):
        """Trainer for NLU."""
        training_data = load_data(self.nlu_training_data)
        trainer = Trainer(config.load(self.nlu_model_config_file))
        trainer.train(training_data)
        model_directory = trainer.persist(self.nlu_model_path,
                                          fixed_model_name='chatbot-001')
        return model_directory

    def train_dialogue(self):
        """Trainer for Dialogue."""
        agent = Agent(self.get_domain_file(),
                      policies=[MemoizationPolicy(max_history=3),
                                ChatBotPolicy()])

        training_data = agent.load_data(self.dialogue_training_data_dir)
        agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
        )

        agent.persist(self.dialogue_model_path)
        return agent
