#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to create quickstart application."""

import logging
from fuzzywuzzy import process
from rasa_core.actions import Action
import requests
import warnings
from .get_user_info import MyProfile
from flask import request
#  from rasa_core.events import SlotSet

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")
WHITE = '\033[32m {} \033[39m'
RED = '\033[31m {} \033[39m'


class CreateQuickStart:
    """Create Application API class."""

    def __init__(self, runtime, mission, application_name, handler, space):
        """Initialize CreateQuickStart class object."""
        self.application_name = application_name
        self.handler = handler
        self.space = space
        self.token = ''
        self.runtime = process.extractOne(
            runtime, ['spring-boot', 'vert.x', 'throntail'])[0]
        self.mission = process.extractOne(
            mission, ['rest-http', 'health-check', 'configmap'])[0]
        self.pipeline = [
            "maven-release",
            "maven-releaseandstage",
            "maven-releasestageapproveandpromote"
        ]
        self.runtime_version = {
            'spring-boot': 'current-redhat',
            'vert.x': 'redhat',
            'throntail': 'redhat'
        }
        self.group_id = {
            'spring-boot': 'spring.boot.application',
            'vert.x': 'vertx.application',
            'throntail': 'thorntail.application'
        }
        self.artifact_id = {
            'spring-boot': 'spring-boot-application',
            'vert.x': 'vertx-application',
            'throntail': 'thorntail-application'
        }
        self.project_version = "1.0.0"
        self.host = 'https://forge.api.openshift.io/api/osio/launch'
        try:
            self.token = request.headers.get('Authorization', '')
        except Exception as exc:
            print(RED.format("No Token Found!\n"), exc)

        if not self.token.startswith('Bearer'):
            self.token = "Bearer {}".format(self.token)

        self.headers = {
            'X-App': "osio",
            'X-Git-Provider': "GitHub",
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': self.token
        }
        __import__('pprint').pprint(self.__dict__)
        __import__('pprint').pprint(vars())

    def get_space_id(self):
        """Get space ID from space name."""
        _base_url = "https://api.openshift.io/api/namedspaces/{u}/{s}"
        _url = _base_url.format(u=self.handler, s=self.space)
        _resp = requests.get(_url)
        if _resp.status_code == 200:
            print(WHITE.format("SUCCESS: openshift spaceID"))
            return _resp.json().get('data', {}).get('id')
        else:
            raise Exception(RED.format(
                "Not able to fetch space name `{}`".format(self.space)))

    def create_booster(self):
        """Create a quickstart booster function."""
        payload = {
            "mission": self.mission,
            "runtime": self.runtime,
            "runtimeVersion": self.runtime_version.get(self.runtime),
            "pipeline": self.pipeline[2],
            "projectName": self.application_name,
            "projectVersion": self.project_version,
            "groupId": self.group_id.get(self.runtime),
            "artifactId": self.artifact_id.get(self.runtime),
            "space": self.get_space_id(),
            "gitRepository": self.application_name
        }
        __import__('pprint').pprint(self.__dict__)
        __import__('pprint').pprint(vars())
        resp = requests.post(self.host, headers=self.headers, data=payload)
        if resp.status_code == 200:
            print(WHITE.format("SUCCESS \n" + str(resp.content)))
            return 'https://openshift.io/{h}/{s}/create/pipelines'\
                .format(h=self.handler, s=self.space)
        else:
            print(RED.format("FAILED \n " +
                             str(resp.status_code) + '\n' + str(resp.content)))


def get_entities(tracker, entites_list):
    """Filter entites from text."""
    entites_set = set(entites_list)
    filtered_entites = {en['entity']: en['value']
                        for en in tracker.latest_message.entities}
    return {en: filtered_entites.get(en) for en in entites_set.intersection(set(filtered_entites))}


def set_slot(tracker, slot_dict):
    """Set value to the slot."""
    for k, v in slot_dict.items():
        tracker._set_slot(k, v)


class CreateQuickStartAction(Action):
    """Action class for deployed applications."""

    def name(self):
        """Return the template name."""
        return 'action_create_quickstart'

    def run(self, dispatcher, tracker, domain):
        """Execute the main logic."""
        self.handler = tracker.get_slot('handler')
        if not self.handler:
            self.handler = MyProfile().handler or ''

        application_name = tracker.get_slot('application_name')
        space_name = tracker.get_slot('space_name')
        runtime = tracker.get_slot('runtime')
        mission = tracker.get_slot('mission')

        if not all([runtime, mission, application_name, self.handler]):
            dispatcher.utter_template("utter_create_quickstart_error", tracker)
            print(RED.format("[runtime, mission, application_name, self.handler]"),
                  [runtime, mission, application_name, self.handler])
            return []

        C = CreateQuickStart(
            runtime, mission, application_name, self.handler, space_name)

        link = C.create_booster()
        if link:
            set_slot(tracker, {'pipeline_link': link})
            dispatcher.utter_template("utter_pipeline_link", tracker)
        else:
            dispatcher.utter_template("utter_create_quickstart_error", tracker)
        return []


class SpaceAction(Action):
    """Space Action class ."""

    def name(self):
        """Return the template name."""
        return 'action_space'

    def run(self, dispatcher, tracker, domain):
        """Execute the main logic."""
        extracted_entites = get_entities(tracker, ['value', 'space_name'])
        if extracted_entites.get('space_name'):
            set_slot(tracker, extracted_entites)
        elif extracted_entites.get('value'):
            set_slot(tracker, {'space_name': extracted_entites.get('value')})
        return []


class RuntimeMissionAction(Action):
    """RUntime Action class ."""

    def name(self):
        """Return the template name."""
        return 'action_runtime_mission'

    def run(self, dispatcher, tracker, domain):
        """Execute the main logic."""
        extracted_entites = get_entities(tracker, ['runtime', 'mission'])
        set_slot(tracker, extracted_entites)
        return []
