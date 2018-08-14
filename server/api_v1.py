#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module for the api endpoints."""

from flask import Blueprint, request
from flask_restful import Api, Resource
from fuzzywuzzy import fuzz
from requests import get
from bot import Bot
from flask_cors import CORS
from .auth import login_required, decode_token

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


def fake_response(query):
    """Generate fake response."""
    # gist url
    url = 'https://gist.githubusercontent.com/invincibleJai/9c4f660fc8e996f1fb6bb01823f937f4\
            /raw/5b431dde29490a72bce85b63d1805036c87dd6d7/chatResponse.json'
    response = get(url).json()

    def _filter(text):
        threshold_point = 50
        match_ratio = fuzz.token_sort_ratio(query, text)
        if match_ratio >= threshold_point:
            return match_ratio, text
        else:
            return -1, ''

    matched_str = sorted(map(_filter, response)).pop()

    __import__('time').sleep(2)

    if matched_str[0] != -1:
        return response.get(matched_str[1])


class ApiEndpoints(Resource):
    """Implementation of / REST API call."""

    def get(self):
        """Handle the GET REST API call."""
        return {'paths': sorted(_resource_paths)}


class ChatBotQuery(Resource):
    """Implementation of /query REST API call."""

    method_decorators = [login_required]

    @staticmethod
    def post():
        """Handle the POST REST API request."""
        bot = Bot()
        input_json = request.get_json()
        decoded_token = decode_token()
        user_name = 'default'
        if decoded_token:
            user_name = decoded_token.get('given_name')

        if not input_json or 'query' not in input_json:
            return dict(error="Expected JSON request and query"), 400

        query = input_json.get('query')
        bot_response = fake_response(query)
        if not bot_response:
            bot_response = bot.run(
                query, message_postprocessor=ChatBotQuery.filter_message, sender_id=user_name)
        return {
            'response': bot_response,
            'timestamp': __import__('time').time()
        }

    @staticmethod
    def filter_message(input_string):
        """Format input string."""
        return '\n'.join([txt['text'] for txt in input_string])


add_resource_no_matter_slashes(ApiEndpoints, '')
add_resource_no_matter_slashes(ChatBotQuery, '/query')
