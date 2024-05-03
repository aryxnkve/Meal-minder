# NutriBuddy

The project aims to develop a personalized meal planner application that utilizes data from various sources, including nutritional databases, user input, and meal suggestion algorithms. The application will be developed using modern web and mobile technologies, leveraging frameworks such as Streamlit for frontend development and FastAPI for backend functionality. The expected deliverables include a user-friendly interface for meal planning, calorie tracking features, personalized meal suggestions, and data visualization capabilities.

## Live application:

http://35.237.26.187:8501/Sign_In

## Documentation

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)]([https://codelabs-preview.appspot.com/?file_id=1r6Cg_miHqOiVv43CM6GhOtq1ZWK9lf6mIlYW7VNuSVk](https://codelabs-preview.appspot.com/?file_id=1IL4wg6ONtgKFOBsyHuDzt-ulIEoyoChsPki4wapNqbM#0))

## Video Demo:

https://youtu.be/_7Gt482oJBc

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
BUCKET_FOLDER_NAME = '<your_folder_name>'
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
