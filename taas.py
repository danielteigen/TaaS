import json
from typing import Text, Tuple
import requests


auth_token = None
running_test_id = None
base_url = 'https://production.vinni.keysight.digital'

URLs = {
    'auth': f'{base_url}/taas-auth',
    'get_campaigns': f'{base_url}/taas/testcampaigns',
    'execute_campaign': f'{base_url}/taas/testcampaigns/{{id}}/{{revision}}/execute',
    'stop_campaign': f'{base_url}/taas/testcampaignexecutions/{{id}}/stop',
    'get_campaign_status': f'{base_url}/taas/testcampaignexecutions/{{id}}/status',
}


class TestCampaign(object):
    def __init__(self, id, name, description, revision, **other_args):
        self.id = id
        self.name = name
        self.description = description
        self.revision = revision

    def __str__(self) -> str:
        return f'{self.id} {self.name}'


campaigns: dict[str, TestCampaign] = {}


def get_auth_token(username: str, password: str) -> Tuple[bool, str]:
    """Returns (success, result)"""
    global auth_token
    headers = {
        'username': username,
        'password': password,
    }
    try:
        response = requests.get(URLs['auth'], headers=headers, timeout=10)
        if response.status_code == 200:
            auth_token = response.text
            return True, 'Auth token received'
        return False, response.text
    except Exception as e:
        return False, f'Connection failed. Check VPN connectivity:\n{e}'


def get_test_campaigns(name: str) -> Tuple[bool, str]:
    """Returns (success, result)
    - On success, the result is a JSON string containing the campaigns
    - On failure, the result is an error message
    """
    params = {'name': name}
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(URLs['get_campaigns'],
                            params=params, headers=headers)
    if response.status_code == 200:
        return True, json.dumps(response.json(), indent=4)
    return False, get_error_code(response)


def execute_test_campaign(name) -> str:
    global running_test_id
    if name not in campaigns:
        return f'The specified campaign "{name}" is not found'
    path_vars = {
        'id': campaigns[name].id,
        'revision': campaigns[name].revision,
    }
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(
        URLs['execute_campaign'].format(**path_vars), headers=headers)
    if response.status_code == 200:
        running_test_id = response.text
        return f'Test started successfully. ID: {running_test_id}'
    return get_error_code(response)


def stop_running_test_campaign() -> str:
    if running_test_id is None:
        return 'Error: no test is running'
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(
        URLs['stop_campaign'].format(id=running_test_id), headers=headers)
    return f'Success {response.text}' if response.status_code == 200 else get_error_code(response)


def get_test_campaign_status() -> str:
    if running_test_id is None:
        return 'Error: no test is running'
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(
        URLs['get_campaign_status'].format(id=running_test_id), headers=headers)
    return json.dumps(response.json(), indent=4) if response.status_code == 200 else get_error_code(response)


def get_error_code(http_response: requests.Response) -> str:
    if auth_token is None:
        return 'No auth token. Please authenticate first'
    return f'{http_response.status_code} {http_response.reason} {str(http_response.content)}'
