import json
import os
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class CharDatabaseInterface:
    """ store the personality of character text"""
    def add_char(self, char_personality: dict):
        """ Adds character personality to database"""
        pass

    def search_char(self, char_personality: dict) -> str:
        """ Searches for character closest to passed in personality """
        pass


class DiscoveryCharDatabase(CharDatabaseInterface):
    api_key = 'hCH8RRcfJEQUE6Ve8gCl_gsXKqM7Mkdusc6Mdnchb51s'
    url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/ed199079-a3d5-47be-ae2c-bac80e6582ae'
    version = '2019-11-22'

    def __init__(self):
        authenticator = IAMAuthenticator(self.api_key)
        self.discovery = DiscoveryV2(
            version=self.version,
            authenticator=authenticator
        )

        self.discovery.set_service_url(self.url)

    def add_char(self, char_personality: dict):
        pass

    def search_char(self, char_personality: dict) -> str:
        pass
