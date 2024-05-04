# NutriBuddy

The project aims to develop a personalized meal planner application that utilizes data from various sources, including nutritional databases, user input, and meal suggestion algorithms. The application will be developed using modern web and mobile technologies, leveraging frameworks such as Streamlit for frontend development and FastAPI for backend functionality. The expected deliverables include a user-friendly interface for meal planning, calorie tracking features, personalized meal suggestions, and data visualization capabilities.

## Live application:

http://35.237.26.187:8501/Sign_In

## Documentation

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1IL4wg6ONtgKFOBsyHuDzt-ulIEoyoChsPki4wapNqbM#0)


## Video Demo:

https://youtu.be/_7Gt482oJBc

## Prerequisites

Make sure to have docker daemon running on your local machine

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

## Steps to run locally

1. Clone the repository on local
```git clone https://github.com/BigDataIA-Summer2023-Team2/Assignment3.git```

2. Create a virtual environment
```python -m venv ./venv```
   
3. Create .env file in following 4 folders:
   - main project directory
   - aiflow/config
   - backend
   - frontend
```
# Snowflake
SNOWFLAKE_USER = '<your_snowflake_user>'
SNOWFLAKE_PASSWORD = '<your_snowflake_passowrd>'
SNOWFLAKE_ACCOUNT = '######-#####'
SNOWFLAKE_WAREHOUSE = 'NUTRIBUDDY_WH'
SNOWFLAKE_DATABASE = 'NUTRIBUDDY_DB'
SNOWFLAKE_SCHEMA = 'PUBLIC'
TABLE_NAME = 'NUTRIBUDDY_DATA'

#GCP
GCP_SERVICE_ACCOUNT_KEY_PATH = './config/gcp_credentials.json'
BUCKET_NAME = '<your_bucket_name>'
BLOB_NAME = '5KRecipes.csv'
BUCKET_FOLDER_NAME = 'recipe_chunks_5k'
CSV_SOURCE_PATH = './config/5KRecipes.csv'

#Pinecone
PINECONE_API_KEY='<pinecone_api_key>'
DISHES_NAMESPACE='recipe_name_5k'
PINECONE_INDEX_NAME='recipes'


# Used in docker-compose.yaml
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=./airflow

#postgres
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_DB='nutribuddy'
POSTGRES_HOST='postgresdb:5432'


# gemini
GOOGLE_API_KEY='<google_key>'
BACKEND_API_URL='http://fastapi:8095'
GCP_SERVICE_ACCOUNT_KEY='gcp_credentials.json'

```

4. Snowflake Setup
   - Sign up for a [Snowflake](https://www.snowflake.com/en/) account
   - Verify Your Email Address
   - You will recieve an activation email with the URL in the below format
     ``` https://<account-identifier>.snowflakecomputing.com/console/login. ```
   - Copy the account identifier from the URL
   - Put your newly created username, password and account identifier in the below .env variables
     ```
     SNOWFLAKE_USER = '<your_snowflake_user>'
     SNOWFLAKE_PASSWORD = '<your_snowflake_passowrd>'
     SNOWFLAKE_ACCOUNT = '######-#####'
     ```
5. Pinecone Setup
   - Sign Up for a [Pinecone](https://www.pinecone.io/) Account
   - Log in and [Generate API key](https://docs.pinecone.io/guides/getting-started/quickstart#2-get-your-api-key)
   - Copy this key and put it in below .env varibale
     ``` PINECONE_API_KEY='<pinecone_api_key>' ```
     
6. Create Google Cloud Storage Bucket
   - Sign in to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a New Project or use an existing one
   - In the Google Cloud Console, navigate to the "Storage" section by clicking on the menu icon in the upper-left corner and selecting "Storage" > "Browser."
   - [Create a Bucket](https://cloud.google.com/storage/docs/creating-buckets)
   - Put your bucket name in the .env variable
     ``` BUCKET_NAME = '<your_bucket_name>' ```

7. Create GCP credentials file
   - Navigate to the IAM & Admin > Service Accounts page in the Google Cloud Console.
   - Click on the "Create Service Account" button.
   - Enter a name and description for the service account.
   - Click on the "Create" button to proceed.
   - Assign the necessary permissions to the service account. To grant full permissions to the bucket, you can assign the "Storage Object Admin" role.
   - Click on the "Continue" button to proceed.
   - Click on the "Create Key" button to generate a new key for the service account.
   - Select the key type as "JSON" and click on the "Create" button.
   - The JSON key file will be generated and downloaded to your computer.
   - Rename this file as "gcp_credentials.json"
   - Put this file the below locations
       - airflow/config
       - backend
       - frontend
         
8. Make sure you have .env file in all the 4 location mentioned before
9. Navigate to the project directory and build the docker images
    ```
   docker compose build
    ```
11. Then run the images as docker containers
     ```
    docker compose up
     ```
    You can also Add the -d flag to run the containers in detached mode (in the background)
    ```
    docker-compose up -d
    ```
13. After running the docker-compose up command, Docker Compose will create and start the containers specified in your docker-compose.yml file. You can verify that the containers are running by executing:
    ```
    docker-compose ps
    ```
    
15. You can now access the application on localhost.
    
16. Run the Airflow pipeline
    - Navigate to ```http://localhost:8080```
    - Use username and password as "airflow" to login
      <img width="662" alt="Screenshot 2024-05-04 at 5 46 40 PM" src="https://github.com/Dalvisayali/NutriBuddy/assets/47607881/200451d3-4bae-4dbf-94c1-ece5a683c40d">
    - Run the "sandbox" DAG by clicking on the play button on right side ("Actions" column)
      <img width="1499" alt="Screenshot 2024-05-04 at 5 48 01 PM" src="https://github.com/Dalvisayali/NutriBuddy/assets/47607881/16969a5d-9a76-4587-9d32-7b1f70cfaabc">

17. Access the application at "http://localhost:8501/Register"

18. Stop and remove the containers as a cleanup step
    ```
    docker-compose down
    ```

## Tools and Technologies:

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Snowflake](https://img.shields.io/badge/snowflake-%234285F4?style=for-the-badge&logo=snowflake&link=https%3A%2F%2Fwww.snowflake.com%2Fen%2F%3F_ga%3D2.41504805.669293969.1706151075-1146686108.1701841103%26_gac%3D1.160808527.1706151104.Cj0KCQiAh8OtBhCQARIsAIkWb68j5NxT6lqmHVbaGdzQYNSz7U0cfRCs-STjxZtgPcZEV-2Vs2-j8HMaAqPsEALw_wcB&logoColor=white)
](https://www.snowflake.com/en/?_ga=2.41504805.669293969.1706151075-1146686108.1701841103&_gac=1.160808527.1706151104.Cj0KCQiAh8OtBhCQARIsAIkWb68j5NxT6lqmHVbaGdzQYNSz7U0cfRCs-STjxZtgPcZEV-2Vs2-j8HMaAqPsEALw_wcB)
[![Apache Airflow](https://img.shields.io/badge/Airflow-yellow?style=for-the-badge&logo=Apache%20Airflow&logoColor=blue)](https://airflow.apache.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=Docker&color=blue&logoColor=white)](https://www.docker.com)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-gray?style=for-the-badge)](https://huggingface.co)



| Name         | Email                        | 
| ------------ | ---------------------------- |
| Ameya Apte   | apte.ame@northeastern.edu    | 
| Sayali Dalvi | dalvi.sa@northeastern.edu    | 
| Soeb Hussain | hussain.soe@northeastern.edu | 

## References

- [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert)
- [Food Recipes Dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/data)
