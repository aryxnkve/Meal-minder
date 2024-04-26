# NutriBuddy

The project aims to develop a personalized meal planner application that utilizes data from various sources, including nutritional databases, user input, and meal suggestion algorithms. The application will be developed using modern web and mobile technologies, leveraging frameworks such as React.js for frontend development and Node.js for backend functionality. The expected deliverables include a user-friendly interface for meal planning, calorie tracking features, personalized meal suggestions, and data visualization capabilities.

## Live application:

http://35.237.26.187:8501/Sign_In

## Documentation

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1r6Cg_miHqOiVv43CM6GhOtq1ZWK9lf6mIlYW7VNuSVk)

## Steps to make it run on your machine

- Clone the github repository on local
- Create env file in ‘./airflow/config’; ‘./backend’; ‘./frontend’; and ‘./’ directories
- Create a virtual environment using ‘python -m venv ./venv’
- Make sure you have docker daemon running on your local machine
- Navigate to the project directory and run ‘docker compose build’ to build the images
- Then execute ‘docker compose up’ to run the images as containers
- To stop the running containers press Ctrl + C / Cmd + C and then execute docker compose down to remove the containers as a cleanup step

## Empty .env structure for './airflow/config', './backend', './frontend' and './'

```
# Used in DAG

SNOWFLAKE_USER = ''
SNOWFLAKE_PASSWORD = ''
SNOWFLAKE_ACCOUNT = ''
SNOWFLAKE_WAREHOUSE = ''
SNOWFLAKE_DATABASE = ''
SNOWFLAKE_SCHEMA = ''
GCP_SERVICE_ACCOUNT_KEY_PATH = ''
BUCKET_NAME = ''
BLOB_NAME = ''
TABLE_NAME_AIRFLOW = ''
CSV_SOURCE_PATH = ''
PINECONE_API_KEY = ''
PINECONE_NAMESPACE_1 = ''
PINECONE_NAMESPACE_2 = ''
PINECONE_INDEX_NAME = ''
OPENAI_API_KEY = ''
EMBEDDING_MODEL = ''
BUCKET_FOLDER_NAME = ''

# Used in docker-compose.yaml

AIRFLOW_UID = 0
AIRFLOW_PROJ_DIR = ''

POSTGRES_USER = ''
POSTGRES_PASSWORD = ''
POSTGRES_DB = ''
POSTGRES_HOST = ''

# PINECONE

DISHES_NAMESPACE = ''
INGREDIENTS_NAMESPACE = ''

# Snowflake

TABLE_NAME = ''

# gemini

GOOGLE_API_KEY = ''
BACKEND_API_URL = ''
```

## Data Sources

### Food.com - Recipes

The recipes dataset contains 522,517 recipes from 312 different categories. This dataset provides information about each recipe like cooking times, servings, ingredients, nutrition, instructions, and more.

## Tools and Technologies:

- FrontEnd : StreamLit
- Backend : FastAPI
- Database : PostGreSQL
- Cloud : GCP
- Create Embeddings: DistilBERT
- Automation : Airflow

## Pipelines

#### Capture Calories:

![Architecture Diagram ](images/1.png)

#### RAG to suggest Meals as per Calories

![Architecture Diagram ](images/2.png)

#### Create Embeddings

![Architecture Diagram ](images/3.png)

## References

- [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert)
