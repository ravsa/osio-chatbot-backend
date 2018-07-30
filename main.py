#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to run the chatbot."""
from bot import Bot, mattermost_runner
from server import ChatBotHTTPServer
import argparse

if __name__ == "__main__":

    bot = Bot()
    http_server = ChatBotHTTPServer()
    parser = argparse.ArgumentParser(description='starts or runs the bot')
    subparser = parser.add_subparsers()
    run = subparser.add_parser('run')
    train = subparser.add_parser('train')
    run.add_argument(
        'run',
        choices=['console', 'mattermost', 'http-server']
    )
    train.add_argument(
        'train',
        choices=['nlu', 'dialogue', 'online', 'all'],
    )

    _input = vars(parser.parse_args())

    if not _input:
        parser.print_help()
    else:
        training = {'nlu': bot.train_nlu,
                    'dialogue': bot.train_dialogue,
                    'online': bot.interactive_training,
                    'all': bot.train
                    }.get(_input.get('train', ''), lambda: None)

        run = {'console': bot.console_run,
               'mattermost': mattermost_runner,
               'http-server': http_server.run
               }.get(_input.get('run', ''), lambda: None)

        training()
        run()
