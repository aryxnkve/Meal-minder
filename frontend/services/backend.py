import os
from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://api:8095")

headers = {'Content-Type': 'application/json'}

def create_user(username, password, firstname, lastname):
    url = f"{BACKEND_API_URL}/api/v1/register_user"
    payload = {
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("username")
    else:
        return False, response.json().get("detail")

def authenticate_user(username, password):
    url = f"{BACKEND_API_URL}/api/v1/user/authenticate"
    payload  = {
        "username": username,
        "password": password
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("auth_token")
    else:
        return False, response.json().get("detail")

def validate_access_token(access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/access_token"
    if not access_token:
        access_token = ""
    payload  = {
        "access_token": access_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("GET", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json().get("name")
    else:
        return False, response.json().get("detail")


