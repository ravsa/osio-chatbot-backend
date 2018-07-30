#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Initialize the package bot."""

import logging
from rasa_core import utils
from .run import Bot
from .plugins import mattermost_runner

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
utils.configure_colored_logging(loglevel="INFO")
