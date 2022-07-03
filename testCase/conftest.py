import pytest
import requests
import os
import sys
from utils import Config_Operation

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(
    current_directory) + os.path.sep + ".")
sys.path.append(root_path)

config = Config_Operation(root_path + os.path.sep + "configs" + os.path.sep + "config.ini")
host = config.get_config("test")['host']
login_url = config.get_config("test")['login_url']


@pytest.fixture(scope="session")
def get_token():
    url = host + login_url
    data = {
        "username": "admin",
        "password": "123456",
        "loginType": "web"
    }
    response = requests.post(url=url, data=data)
    token = response.json()["data"]["token"]
    return token


if __name__ == '__main__':

    get_token()