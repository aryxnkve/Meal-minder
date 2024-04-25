import os
from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError
import time
from PIL import Image

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://api:8095")

headers = {'Content-Type': 'application/json'}

def create_user(info):
    url = f"{BACKEND_API_URL}/api/v1/register_user"
    payload = info
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

def set_user_preferences(preferences):
    url = f"{BACKEND_API_URL}/api/v1/user/preferences"

    payload = dict()
    payload["access_token"] = preferences['access_token']
    payload["is_vegetarian"] = preferences['is_vegetarian']
    payload['cuisine'] = ', '.join(preferences['cuisine'])
    payload['dishes'] = ', '.join(preferences['dishes'])
    payload['ingredients'] = ', '.join(preferences['ingredients'])
    payload['allergies'] = ', '.join(preferences['allergies'])
    
    json_payload = json.dumps(payload)
    print("Preferences payload = ", payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True
    else:
        return False, response.json().get("detail")
    
def get_user_preferences(auth_token):
    url = f"{BACKEND_API_URL}/api/v1/user/get-preferences"

    payload = {
        "access_token": auth_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, ""
    
def get_suggested_dishes(auth_token):
    url = f"{BACKEND_API_URL}/api/v1/user/suggest-dish"

    payload = {
        "access_token": auth_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")

def get_remaining_calories(auth_token):
    url = f"{BACKEND_API_URL}/api/v1/user/get-remaining-calories"

    payload = {
        "access_token": auth_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, ""


def get_report_data(auth_token):
    url = f"{BACKEND_API_URL}/api/v1/user/get-report-data"

    payload = {
        "access_token": auth_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")
    
    
def get_calorie_count(image,label, access_token):
    url = f"{BACKEND_API_URL}/api/v1/user/calorie_count"
    payload = dict()

    payload["access_token"] = access_token
    payload["label"] = label
    payload["image"] = image

    json_payload = json.dumps(payload)
    print("Preferences payload = ", payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True
    else:
        return False, response.json().get("detail")


def get_calorie(image, description):
    url = f"{BACKEND_API_URL}/api/v1/user/calorie_count"
    headers = {'Accept': 'application/json'}
    params = {'description': description}
    files = {'file': ('uploaded_image.png', image, 'image/png')}
    
    response = requests.post(url, headers=headers, params=params, files=files)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, ""

def resize_image(image):
    # Convert the file to an Image object
    image = Image.open(image)
    # Resize the image to 25% of its original size
    image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
    return image

def insert_calories(auth_token,dishname,calorie,gcplink= 'https://nhi.com'):
    url = f"{BACKEND_API_URL}/api/v1/user/insert_calorie"

    payload = dict()
    payload["access_token"] = auth_token
    payload["dish_name"] = dishname
    payload['calories'] = str(calorie)
    payload['file_link'] = gcplink

    payload['timestamp'] = str(datetime.now())

    json_payload = json.dumps(payload)
    print("weekly calories payload = ", payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("detail")
    


    



