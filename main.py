#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to run the chatbot."""
from bot import Bot, mattermost_runner
import argparse


if __name__ == "__main__":

    bot = Bot()
    parser = argparse.ArgumentParser(description='starts the bot')
    parser.add_argument(
        'task',
        choices=["train-nlu", "train-dialogue", "train-all",
                 "train-online", "run-console", "run-mattermost"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    if task == "train-nlu":
        bot.train_nlu()
    elif task == "train-dialogue":
        bot.train_dialogue()
    elif task == "train-online":
        bot.interactive_training()
    elif task == "train-all":
        bot.train()
    elif task == "run-console":
        bot.console_run()
    elif task == "run-mattermost":
        mattermost_runner()
