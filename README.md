# NutriBuddy

The project aims to develop a personalized meal planner application that utilizes data from various sources, including nutritional databases, user input, and meal suggestion algorithms. The application will be developed using modern web and mobile technologies, leveraging frameworks such as Streamlit for frontend development and FastAPI for backend functionality. The expected deliverables include a user-friendly interface for meal planning, calorie tracking features, personalized meal suggestions, and data visualization capabilities.

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

### [Food.com - Recipes](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/data)

The recipes dataset contains 522,517 recipes from 312 different categories. This dataset provides information about each recipe like cooking times, servings, ingredients, nutrition, instructions, and more.

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

## Pipelines

#### Capture Calories:

![Architecture Diagram ](images/1.png)

#### RAG to suggest Meals as per Calories

![Architecture Diagram ](images/2.png)

#### Create Embeddings

![Architecture Diagram ](images/3.png)

## Big Data Systems and Intelligence Analytics (DAMG 7245)

| Name         | Email                        | NUID    | Contribution |
| ------------ | ---------------------------- | ------- | ------------ |
| Ameya Apte   | apte.ame@northeastern.edu    | 2764540 | 33%          |
| Sayali Dalvi | dalvi.sa@northeastern.edu    | 2799803 | 34%          |
| Soeb Hussain | hussain.soe@northeastern.edu | 2747200 | 33%          |

## References

- [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert)
- [Food Recipes Dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews/data)
