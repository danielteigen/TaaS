import requests


auth_token = None
base_url = 'https://production.vinni.keysight.digital'

URLs = {
    'auth': f'{base_url}/taas-auth',
    'get_campaigns': f'{base_url}/taas/testcampaigns',
}


def get_auth_token(username: str, password: str) -> str:
    global auth_token
    headers = {
        'username': username,
        'password': password,
    }
    response = requests.get(URLs['auth'], headers=headers)
    if response.status_code == 200:
        auth_token = response.text
        return 'Auth token received'
    return response.text


def get_test_campaigns(name: str) -> str:
    params = {}
    if name:
        params = {'name': name}
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(URLs['get_campaigns'],
                            params=params, headers=headers)
    return response.text if response.status_code == 200 else get_error_code(response)


def get_error_code(http_response: requests.Response) -> str:
    if auth_token is None:
        return 'No auth token. Please authenticate first'
    return f'{http_response.status_code} {http_response.reason}'
