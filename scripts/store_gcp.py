from google.cloud import storage
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

env_path = 'C:/Users/aptea/OneDrive/Documents/NEU/Sem6/BDIA/NutriBuddy/scripts/.env'
load_dotenv(dotenv_path=env_path)

def upload_file_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file):
    """Uploads a file to a GCS bucket."""
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

# Example usage
bucket_name = os.getenv('BUCKET_NAME')
source_file_path = os.getenv('CSV_SOURCE_PATH')
destination_blob_name = os.getenv('BLOB_NAME')
credentials_file = os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH')

upload_file_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file)
