import json
from typing import Text
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


def get_auth_token(username: str, password: str) -> str:
    global auth_token
    headers = {
        'username': username,
        'password': password,
    }
    try:
        response = requests.get(URLs['auth'], headers=headers)
        if response.status_code == 200:
            auth_token = response.text
            return 'Auth token received'
        return response.text
    except Exception as e:
        return f'Connection failed. Check VPN connectivity:\n{e}'


def get_test_campaigns(name: str) -> str:
    params = {}
    if name:
        params = {'name': name}
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(URLs['get_campaigns'],
                            params=params, headers=headers)
    return json.dumps(response.json(), indent=4) if response.status_code == 200 else get_error_code(response)


def execute_test_campaign(id, revision) -> str:
    global running_test_id
    path_vars = {
        'id': id,
        'revision': revision,
    }
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(
        URLs['execute_campaign'].format(**path_vars), headers=headers)
    if response.status_code == 200:
        running_test_id = response.text
        return f'Test run successfully. ID: {running_test_id}'
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
