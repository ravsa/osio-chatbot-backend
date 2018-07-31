#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configurations."""
import os

TESTING = False
DEBUG = True
BAYESIAN_JWT_AUDIENCE = os.environ.get("BAYESIAN_JWT_AUDIENCE", "")
BAYESIAN_FETCH_PUBLIC_KEY = os.environ.get("BAYESIAN_FETCH_PUBLIC_KEY", "")
DISABLE_AUTHENTICATION = os.environ.get("DISABLE_AUTHENTICATION", "")
