"""
Functions to config and initialise the system. Expects environment variables for most
"""

import json
import os
import logging  # noqa


from performance.tests.fixtures import get_sample_rp_mapping  # TODO fixture should move in here


# logging.basicConfig(level=logging.DEBUG)  #noqa

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    ENV = 'prod'

    VERIFY_DATA_PIPELINE_CONFIG_PATH = os.path.abspath(
        os.path.join(BASE_DIR, '..', 'verify-data-pipeline-config'))
    PIWIK_PERIOD = 'week'
    PIWIK_LIMIT = '-1'
    PIWIK_BASE_URL = 'https://analytics-hub-prod-a-dmz.ida.digital.cabinet-office.gov.uk/index.php'
    DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, 'output')
    GSHEETS_CREDENTIALS_FILE = os.path.join(
        VERIFY_DATA_PIPELINE_CONFIG_PATH, 'credentials', 'google_sheets_credentials.json')

    def __init__(self):
        # TODO: grab these from ENV variables
        self.PIWIK_AUTH_TOKEN = self._get_piwik_token()
        self.rp_information = {rp['rp_name']: rp for rp in self._load_json_configuration('rp_information')}
        self.rp_mapping = self._load_json_configuration('rp_mapping')
        self._validate_rp_information()

    def _get_piwik_token(self):
        with open(f'{self.VERIFY_DATA_PIPELINE_CONFIG_PATH}/credentials/piwik_token.json') as fileHandle:
            token = json.load(fileHandle)['production' if self.ENV == 'prod' else 'dr_token']
            return token

    def _load_json_configuration(self, name):
        config_file = os.path.join(self.VERIFY_DATA_PIPELINE_CONFIG_PATH, 'configuration', '{}.json'.format(name))
        with open(config_file) as f:
            return json.load(f)

    def _validate_rp_information(self):
        diff = set(self.rp_information.keys()).symmetric_difference(self.rp_mapping.values())
        if diff:
            raise LookupError('RP information and RP mappings are different:', diff)


# TODO should the below move into a JSON file?
_sample_rp_information = [
    {
        "rp_name": "RP 1",
        "department": "RP1 dept",
        "service_description": "RP1 description",
        "loa": "LOA_2",
        "sheet_key": "1234ABCD"
    },
    {
        "rp_name": "RP 2",
        "department": "RP2 dept",
        "service_description": "RP2 description",
        "loa": "LOA_2",
        "sheet_key": "1234ABCD"
    },
    {
        "rp_name": "RP 3",
        "department": "RP3 dept",
        "service_description": "RP3 description",
        "loa": "LOA_2",
        "sheet_key": "1234ABCD"
    },
    {
        "rp_name": "RP 4",
        "department": "RP4 dept",
        "service_description": "RP4 description",
        "loa": "LOA_2",
        "sheet_key": "1234ABCD"
    },
]


class TestConfig(Config):
    ENV = 'test'

    def __init__(self):
        self.PIWIK_AUTH_TOKEN = "DUMMY_PIWIK_TOKEN"
        self.rp_information = {rp['rp_name']: rp for rp in _sample_rp_information}
        self.rp_mapping = get_sample_rp_mapping()
        self._validate_rp_information()