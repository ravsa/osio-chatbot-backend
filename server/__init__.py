#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Initialize module for server."""

from flask import Flask, redirect, url_for
from flask_appconfig import AppConfig
from gunicorn.app.base import Application
from .api_v1 import app_v1
import multiprocessing
import os


app = Flask(__name__)
AppConfig(app)
app.register_blueprint(app_v1)


@app.route('/')
def base_url():
    """Redirect / to /api/v1 url."""
    return redirect(url_for('api_v1.apiendpoints__slashless'))


def number_of_workers():
    """Return the number_of_workers [(cores * 2) +1 ]."""
    return (multiprocessing.cpu_count() * 2) + 1


class ChatBotHTTPServer(Application):
    """ChatBotHTTPServer Flask applicaiton."""

    def init(self, parser, opts, args):
        """Initialize the all parameters."""
        self.host = os.getenv("HTTP_SERVER_HOST", '0.0.0.0')
        self.port = os.getenv("HTTP_SERVER_PORT", '8008')
        return {
            'bind': '{0}:{1}'.format(self.host, self.port),
            'workers': int(os.getenv("HTTP_SERVER_WORKERS", number_of_workers()))
        }

    def load(self):
        """Load the application."""
        return app
