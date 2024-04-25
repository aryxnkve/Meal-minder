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
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://api:8095")

headers = {'Content-Type': 'application/json'}

# Google Cloud Storage credentials and bucket
BUCKET_NAME = os.getenv('BUCKET_NAME')
CREDENTIALS_PATH = os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH')

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
    

def get_calorie(image):
    url = f"{BACKEND_API_URL}/api/v1/user/calorie_count"
    headers = {'Accept': 'application/json'}
    files = {'file': ('uploaded_image.png', image, 'image/png')}
    
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, ""

def resize_image(image):
    # Convert the file to an Image object
    image = Image.open(image)
    image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
    return image

def insert_calories(auth_token,dishname,calorie,gcplink):
    print("Here")
    url = f"{BACKEND_API_URL}/api/v1/user/insert_calorie"

    payload = dict()
    payload["access_token"] = auth_token
    payload["dish_name"] = dishname
    payload['calories'] = int(calorie)
    payload['file_link'] = gcplink

    payload['timestamp'] = datetime.now().isoformat()

    json_payload = json.dumps(payload)
    print("weekly calories payload = ", payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True
    else:
        return False
            
def upload_image_to_gcs(image_file, destination_blob_name):
   # Auth using service account credentials
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(f'images/{destination_blob_name}')
    blob.upload_from_string(image_file.getvalue(), content_type=image_file.type)
    
    return blob.public_url

def get_user_daily_calories(auth_token):
    url = f"{BACKEND_API_URL}/api/v1/user/get-user-calorie-goal"

    payload = {
        "access_token": auth_token
    }
    json_payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=json_payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, ""

