#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for the api endpoints."""

from flask import Blueprint, request
from flask_restful import Api, Resource
from bot import Bot
from flask_cors import CORS
#  from .auth import login_required, decode_token

app_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
rest_api = Api(app_v1)
CORS(app_v1)
_resource_paths = list()


def add_resource_no_matter_slashes(resource, route,
                                   endpoint=None, defaults=None):
    """Add resource and ignore slashes."""
    slashless = route.rstrip('/')
    _resource_paths.append(app_v1.url_prefix + slashless)
    slashful = route + '/'
    endpoint = endpoint or resource.__name__.lower()
    defaults = defaults or {}

    rest_api.add_resource(resource,
                          slashless,
                          endpoint=endpoint + '__slashless',
                          defaults=defaults)
    rest_api.add_resource(resource,
                          slashful,
                          endpoint=endpoint + '__slashful',
                          defaults=defaults)


class ApiEndpoints(Resource):
    """Implementation of / REST API call."""

    def get(self):
        """Handle the GET REST API call."""
        return {'paths': sorted(_resource_paths)}


class ChatBotQuery(Resource):
    """Implementation of /query REST API call."""

    #  method_decorators = [login_required]

    @staticmethod
    def post():
        """Handle the POST REST API request."""
        bot = Bot()
        input_json = request.get_json()
        #  decoded_token = decode_token()

        if not input_json or 'query' not in input_json:
            return dict(error="Expected JSON request and query"), 400

        query = input_json.get('query')

        bot_response = bot.run(
            query, message_postprocessor=ChatBotQuery.filter_message)

        return {
            'response': bot_response,
            'timestamp': __import__('time').time(),
        }

    @staticmethod
    def filter_message(input_string):
        """Format input string."""
        return '\n'.join([txt['text'] for txt in input_string])


add_resource_no_matter_slashes(ApiEndpoints, '')
add_resource_no_matter_slashes(ChatBotQuery, '/query')
