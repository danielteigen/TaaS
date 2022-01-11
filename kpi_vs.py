
import json
import requests


def get_url(usecase: str) -> str:
    """Return the URL matching the passed usecase"""
    if usecase not in ['1.3', '1.5', '3.1', '3.2', '3.5', '3.6']:
        raise ValueError(f'{usecase} is not a valid usecase')
    return f'https://ingress02.kpivs-5gsolutions.eu/api/_5g/ucPerformTest_{usecase.replace(".", "")}'


def send_requst(username, password, test_id, usecase) -> str:
    headers = {
        'username': username,
        'password': password,
    }
    url = get_url(usecase)
    data = {
        "test_id": test_id,
        "living_lab": "LL3",
        "use_case": f"UC{usecase}",
    }
    response = requests.post(
        url, json=json.dumps(data), headers=headers)
    return f'Success {response.text}' if response.status_code == 200 else get_error_code(response)


def get_error_code(http_response: requests.Response) -> str:
    return f'{http_response.status_code} {http_response.reason} {str(http_response.content)}'
