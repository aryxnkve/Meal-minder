import requests
import json
from helpers import gemini_helper
import re
import csv
import os

from google.oauth2 import service_account

# Google Cloud Storage credentials and bucket
BUCKET_NAME = os.getenv('BUCKET_NAME')
CREDENTIALS_PATH = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
blob_name = 'report'
local_file_path = 'data/calorie_comparison.csv'

def count_calories(file):
    result = ''
    result = gemini_helper.vision_calorie(file)
    print(result)
    try:
        ingredient_calories, dish_name = parse_ingredients(result)
        total_nutrition_cal = 0

        all_food_data = []
        for ingredient, calorie in ingredient_calories:
            food_data = {
                'dish_name': dish_name,
                'ingredient': ingredient,
                'gemini_calories': calorie,
                'nutrition_api_calories': 0
            }
            food_data['nutrition_api_calories'] = call_nutrition_api(ingredient)
            total_nutrition_cal += food_data['nutrition_api_calories']
            all_food_data.append(food_data)
        print(all_food_data)
        # store to csv


        # Download the file if it exists, otherwise create a new one
        exists = download_blob_to_file(BUCKET_NAME, blob_name, local_file_path)

        # Update the CSV file with new data or create it if it doesn't exist
        update_csv_file(local_file_path, all_food_data)

        # Upload the updated or new file back to Google Cloud Storage
        upload_blob_from_file(BUCKET_NAME, local_file_path, blob_name)
    except Exception as e:
        print("Some error ocurred while process nutrition api : ", str(e))
        return {"response": result, "total_nutrition_cal": 0}

    return {"response": result, "total_nutrition_cal": total_nutrition_cal}

def parse_ingredients(recipe_text):
    # Extract ingredients and their corresponding calorie information
    name = re.search(r"\*\*Name:\*\*\s*(.*?)\s*\n", recipe_text)
    print(name)
    name = name.group(1)
    # ingredients = re.findall(r'- (.*?)(?:\n|$)', recipe_text.split('**Calories Per Ingredient:**')[0])
    calories = re.findall(r'- (.*?): (\d+) calories', recipe_text.split('**Calories Per Ingredient:**')[1])

    print(name)
    # print(ingredients)
    print(calories)
    # Convert calorie tuples from string to int for calorie values
    calories = [(item, int(cal)) for item, cal in calories]

    # Zip ingredients and calories into a list of tuples
    # ingredient_calories = list(zip(ingredients, [cal for _, cal in calories]))

    # Print the list of ingredients with their corresponding calories
    print("Ingredients and their corresponding calories:")
    for ingredient, calorie in calories:
        print(f"{ingredient}: {calorie} calories")
    return calories, name


def call_nutrition_api(ingredients):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': 'ce9b049e',  # Replace 'YOUR_APP_ID' with your actual app ID
        'x-app-key': 'b0794a6f7cd29f8fcda92667395524d8'  # Replace 'YOUR_APP_KEY' with your actual app key
    }
    data = {
        "query": ingredients
    }

    response = requests.post(url, headers=headers, json=data)
    res = json.loads(response.text)

    return (res['foods'][0]['nf_calories'])


from google.cloud import storage
def download_blob_to_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    if blob.exists():
        blob.download_to_filename(destination_file_name)
        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
        return True
    else:
        print(f"Blob {source_blob_name} does not exist.")
        return False

def upload_blob_from_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def update_csv_file(file_name, data):
    """Updates or creates a CSV file with new data."""
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    except FileNotFoundError:
        existing_data = []

    with open(file_name, mode='w', newline='') as file:
        fieldnames = ['dish_name', 'ingredient', 'gemini_calories', 'nutrition_api_calories']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write header if file is new or existing
        writer.writerows(existing_data)  # Write existing data
        writer.writerows(data)  # Append new data from list of dictionaries
