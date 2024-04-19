from fastapi import APIRouter
from dotenv import dotenv_values
import time
import logging

router = APIRouter()

config = dotenv_values(".env")

from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

AIRFLOW_API_URL = config["AIRFLOW_API_URL"]
AIRFLOW_USERNAME = config["AIRFLOW_USERNAME"]
AIRFLOW_PASSWORD = config["AIRFLOW_PASSWORD"]

from requests.auth import HTTPBasicAuth


@router.get("/trigger_airflow_pipeline/")
async def trigger_airflow_dag(host, dag_id,username,password):
    # Construct the URL
    url = f"http://{host}/api/v1/dags/{dag_id}/dagRuns"

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Data payload for the request
    data = {"conf": {}}

    # Basic authentication credentials
    username = "airflow"
    password = "airflow"

    # Make the POST request
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))

    # Check the response status and return the result
    if response.status_code == 200:
        print("success")
        return response.json()  # Return the response as JSON if the request was successful
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
        print('not success')
        return {"status": "Failure", "error": response.text}  # Return an error message if the request failed



def trigger_pipeline(s3_file_path):
    return True
    # try: 
    #     # Prepare headers for Basic Authentication
    #     headers = {'Content-Type': 'application/json'}
    #     auth = (AIRFLOW_USERNAME, AIRFLOW_PASSWORD)

    #     # Prepare data to trigger the DAG
    #     data = {
    #         "conf": {"s3_file_path": s3_file_path}  # Pass any additional parameters needed by your DAG
    #     }
    #     # Trigger the Airflow DAG
    #     response = requests.post(AIRFLOW_API_URL, headers=headers, json=data, auth=auth)
    #     logging.info(f"Airflow response: {response}")
    #     if response.status_code == 200:
    #         return True
    #     else:
    #         logging.error("Some error occurred")
    #         return False

    # except Exception as e:
    #     logging.error(str(e))
    #     return False



@router.get("/pipeline_status/")
async def get_pipeline_status():
    status = get_status()
    if status:
        return {"status": "Success", "message": "Airflow pipeline status retrieved successfully", "airflow_status": status}
    else:
        return {"status": "Failure", "error": "Something went wrong"}
    
    
def get_status():
    airflow_url = AIRFLOW_API_URL
    try:
        response = requests.get(f"{airflow_url}/health")
        if response.status_code == 200:
            data = response.json()
            # Creating a summary of the health status for each component
            statuses = []
            for component, details in data.items():
                status = details['status']
                if status is None:
                    status = 'No status'
                statuses.append(f"{component}: {status}")
            # Joining all statuses into a single string for display
            return '\n'.join(statuses)
        else:
            return "Airflow server returned an error."
    except Exception as e:
        return str(e)




