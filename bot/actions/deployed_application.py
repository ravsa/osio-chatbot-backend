#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module to get deployed application information."""

import logging
from rasa_core.actions import Action
from rasa_core.events import SlotSet
from fuzzywuzzy import process

logger = logging.getLogger(__name__)


class DeployedApplications:
    """Deployed Application API class."""

    def get_deployment_status(self, application_name):
        """Get the deployment status of the application.

        application_name: String
        return: application build status as String
        """
        return self.search_application(application_name).get('build_status',
                                                             'Applicaiton Not found!')

    def search_application(self, application_name):
        """Search for the application informations.

        application_name: String
        return: application information as Dict Ojbect
        """
        # dummy applications
        applicaitons = [
            {
                'name': 'springboot-applicaiton',
                'build_status': 'passed'
            },
            {
                'name': 'vertx-applicaiton',
                'build_status': 'failed'
            },
            {
                'name': 'thoretail-applicaiton',
                'build_status': 'running'
            }
        ]
        applicaitons_dict = {item['name']: item for item in applicaitons}
        processed = process.extractOne(
            application_name, applicaitons_dict.keys())
        if processed[1] > 80:
            return applicaitons_dict.get(processed[0])
        return {}


class FindDeployedApplication(Action):
    """Action class for deployed applications."""

    def name(self):
        """Return the template name."""
        return 'action_find_deployed_application'

    def run(self, dispatcher, tracker, domain):
        """Run method to execute action."""
        dispatcher.utter_message("searching for application")
        deployed_application = DeployedApplications()
        status = deployed_application.get_deployment_status(
            tracker.get_slot("application_name"))
        return [SlotSet("deployment_status", status)]
