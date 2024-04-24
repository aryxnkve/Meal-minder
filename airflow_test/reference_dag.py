import os
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta
from typing import List, Tuple

from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
import time
import sys
import pandas as pd
import csv
from openai import OpenAI
import re
from pinecone import Pinecone, PodSpec
import numpy as np
import snowflake.connector
from snowflake.connector import DictCursor
import openai
from tqdm import tqdm 
current_directory = os.getcwd()
sys.path.append(current_directory)


##### TryS
from google.cloud import storage
import io
import pinecone
from pinecone import Pinecone, ServerlessSpec, PodSpec
from transformers import DistilBertModel, DistilBertTokenizer
import torch
import math
import concurrent.futures

# Load environment variables
load_dotenv('./config/.env',override=True)

# Google Cloud Storage credentials and bucket
credentials_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH')
bucket_name = os.getenv('BUCKET_NAME')

# Local file path
local_file_path = os.getenv('CSV_SOURCE_PATH')

def upload_csv2gcp_main():




    # Function to upload a file to Google Cloud Storage
    def upload_to_gcs(file_path, blob_name):
        storage_client = storage.Client.from_service_account_json(credentials_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        print(f"File uploaded to {blob_name}")

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(local_file_path)

    # Split the DataFrame into smaller chunks (e.g., 100 rows per chunk)
    chunk_size = 500
    chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

    # Upload each chunk as a separate CSV file to Google Cloud Storage
    for i, chunk in enumerate(chunks):
        # Convert chunk to CSV
        chunk_csv_path = f"./scripts/data/chunk_{i+1}.csv"
        chunk.to_csv(chunk_csv_path, index=False)
        
        # Upload CSV to Google Cloud Storage
        blob_name = f"chunks7/chunk_{i+1}.csv"  # Specify the blob name (e.g., a directory path)

        retry = 15
        retryIndicator = True
        while retry > 0 and retryIndicator:
            try :
                upload_to_gcs(chunk_csv_path, blob_name)
                retryIndicator = False
            except Exception as e:
                print(str(e))
                time.sleep(5)
                retry -=1
                print('error in' +  str(retry))
    
def upload_gcp2snowflake_main():
    
    # Function to get Snowflake data type from pandas data type
    def get_snowflake_data_type(dtype):
        if dtype == 'object':
            return 'VARCHAR'
        elif dtype == 'int64':
            return 'INT'
        elif dtype == 'float64':
            return 'FLOAT'
        else:
            return 'VARCHAR'

    # Set up GCP credentials
    service_account_key_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY_PATH')
    storage_client = storage.Client.from_service_account_json(service_account_key_path)

    # Set up Snowflake connection parameters
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
    table_name = os.getenv('TABLE_NAME')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

    # Cursor to execute SQL queries
    cur = conn.cursor()

    # Access the CSV files in the GCP bucket
    bucket_name = os.getenv('BUCKET_NAME')
    folder_name = 'chunks7'  # Name of the folder inside the bucket

    # List all blobs (files) in the folder
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)

    # Convert the iterator to a list
    blobs_list = list(blobs)

    # Read the first CSV file to create the table
    first_blob = blobs_list[0]
    csv_data = io.BytesIO(first_blob.download_as_string())
    df = pd.read_csv(csv_data, dtype=str, na_values=['NaN', 'NAN', ''])
    df = df.fillna('')
    print("Debug size cleaned csv", df.shape)
    create_table_sql = f"CREATE OR REPLACE TABLE {table_name} ("
    for column_name, dtype in zip(df.columns, df.dtypes):
        snowflake_dtype = get_snowflake_data_type(str(dtype))
        create_table_sql += f"{column_name} {snowflake_dtype}, "
    create_table_sql = create_table_sql[:-2] + ")"
    cur.execute(create_table_sql)

    # Loop through each blob (file) in the folder (excluding the first one)
    for blob in tqdm(blobs_list, desc='Processing CSV files', unit='file'):
        # Read the CSV data as a file-like object
        csv_data = io.BytesIO(blob.download_as_string())
        
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_data, dtype=str, na_values=['NaN', 'NAN', ''])  # Convert NaN values to empty strings
        df = df.fillna('')
        print("Debug size cleaned csv", df.shape)
        # Generate the INSERT INTO statement
        insert_into_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s']*len(df.columns))})"
        
        # Execute the INSERT INTO statement
        cur.executemany(insert_into_sql, df.values.tolist())

    # Commit the transaction
    conn.commit()

    # Close Snowflake connection
    cur.close()
    conn.close()

def upload_embeddings2pinecone(*op_args):

    # Create or retrieve a namespace in Pinecone
    namespace_name = op_args[0]
    column_name = op_args[1]
    index_name = os.getenv('PINECONE_INDEX_NAME')
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    # Check whether the index with the same name already exists - if so, delete it
    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(name=index_name, dimension=768, spec=PodSpec(environment="gcp-starter"))
    index = pinecone.Index(name=index_name)
    print(namespace_name, column_name, index)
    # Load the DistilBERT model and tokenizer
    model_name = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name)

    # Snowflake connection parameters
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

    # Cursor to execute SQL queries
    cur = conn.cursor()
    table_name = os.getenv('TABLE_NAME')

    # Get the total number of rows in the table
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]
    # total_rows = 100000

    # Define the batch size
    batch_size = 100

    # Calculate the number of batches needed
    num_batches = math.ceil(total_rows / batch_size)

    def process_batch(batch_index):
    # offset = (batch_index * batch_size)
        offset = (batch_index * batch_size)
        cur.execute(f"SELECT {column_name}, recipeid FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        # cur.execute(f"SELECT name, recipeid FROM {table_name}")
        results = cur.fetchall()
        texts = [result[0] for result in results]
        ids = [result[1] for result in results]
        # print(texts, ids)
        if(len(ids) > 0 ):
            # print("I am here 1")
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            # print(inputs)
            # print("I am here 2")
            with torch.no_grad():
                # print("I am here torch 1")
                outputs = model(**inputs)
                # print(outputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
                # print(embeddings)
            # print("I am here 3")
            vectors = [(ids[i], embeddings[i]) for i in range(len(ids))]
            print(f"Uploading vectors for batch {batch_index + 1}..")
            # print("I am here 4")
            retry = 15
            retryIndicator = True
            while retry > 0 and retryIndicator:
                try :
                    # print("I am here 5")
                    res = index.upsert(vectors=vectors, namespace=namespace_name)
                    # print(res)
                    retryIndicator = False
                    # print("I am here 6")
                except Exception as e:
                    # print("I am here 7") 
                    print( 'error in upsert retry for '+ namespace_name + "   ---> " + str(e) )
                    time.sleep(5)
                    retry -=1
                    print('error in' +  str(retry))
                    # print("I am here 8")
        # print("I am here 9")
    # Use ThreadPoolExecutor to process batches concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_batch, i) for i in range(num_batches)]
        if(len(futures)> 0):
            for future in concurrent.futures.as_completed(futures):
                print("I am here multi 1")
                future.result()
                print("I am here multi 2")
    # print("I am here 10")
    # Close Snowflake connection
    cur.close()
    conn.close()
    # print("I am here 11")

def upload_embeddings2pinecone_test(*op_args):

    # Create or retrieve a namespace in Pinecone
    namespace_name = op_args[0]
    column_name = op_args[1]
    index_name = os.getenv('PINECONE_INDEX_NAME')
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    # Check whether the index with the same name already exists - if so, delete it
    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(name=index_name, dimension=768, spec=PodSpec(environment="gcp-starter"))
    index = pinecone.Index(name=index_name)
    print(namespace_name, column_name, index)
    # Load the DistilBERT model and tokenizer
    model_name = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name)

    # Snowflake connection parameters
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

    # Cursor to execute SQL queries
    cur = conn.cursor()
    table_name = os.getenv('TABLE_NAME')

    # Get the total number of rows in the table
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]
    # total_rows = 100000

    # Define the batch size
    batch_size = 20

    # Calculate the number of batches needed
    num_batches = math.ceil(total_rows / batch_size)

    # def process_batch(batch_index):
    # offset = (batch_index * batch_size)
    i = 0
    while(i <= num_batches):
        offset = (i* batch_size)
        cur.execute(f"SELECT {column_name}, recipeid FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        # cur.execute(f"SELECT name, recipeid FROM {table_name}")
        results = cur.fetchall()
        texts = [result[0] for result in results]
        ids = [result[1] for result in results]
        # print(texts, ids)
        if(len(ids) > 0 ):
            # print("I am here 1")
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            # print(inputs)
            # print("I am here 2")
            with torch.no_grad():
                # print("I am here torch 1")
                outputs = model(**inputs)
                # print(outputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
                # print(embeddings)
            # print("I am here 3")
            print("Debug len ids", len(ids))
            vectors = [(ids[i], embeddings[i]) for i in range(len(ids))]
            # print(f"Uploading vectors for batch {num_batches + 1}..")
            # print("I am here 4")
            retry = 15
            retryIndicator = True
            while retry > 0 and retryIndicator:
                try :
                    # print("I am here 5")
                    res = index.upsert(vectors=vectors, namespace=namespace_name)
                    print(res)
                    retryIndicator = False
                    # print("I am here 6")
                except Exception as e:
                    # print("I am here 7") 
                    print( 'error in upsert retry for '+ namespace_name + "   ---> " + str(e) )
                    time.sleep(5)
                    retry -=1
                    print('error in' +  str(retry))
                    # print("I am here 8")
        i = i + 1
    # print("I am here 9")
    # Use ThreadPoolExecutor to process batches concurrently
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(process_batch, i) for i in range(num_batches)]
    #     if(len(futures)!=0):
    #         for future in concurrent.futures.as_completed(futures):
    #             print("I am here multi 1")
    #             future.result()
    #             print("I am here multi 2")
    # print("I am here 10")
    # Close Snowflake connection
    print("Debug num vectors", index.describe_index_stats())
    cur.close()
    conn.close()
    # print("I am here 11")

def upload_embeddings2pinecone3(*op_args):

    # Create or retrieve a namespace in Pinecone
    namespace_name1 = op_args[0]
    namespace_name2 = op_args[1]
    recipe_name = op_args[2]
    ingredient_name = op_args[3]
    index_name = os.getenv('PINECONE_INDEX_NAME')
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    # Check whether the index with the same name already exists - if so, delete it
    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(name=index_name, dimension=768, spec=PodSpec(environment="gcp-starter"))
    index = pinecone.Index(name=index_name)

    # Load the DistilBERT model and tokenizer
    model_name = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name)

    # Snowflake connection parameters
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

    # Cursor to execute SQL queries
    cur = conn.cursor()
    table_name = os.getenv('TABLE_NAME')

    # Get the total number of rows in the table
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]
    # total_rows = 100000

    # Define the batch size
    batch_size = 100

    # Calculate the number of batches needed
    num_batches = math.ceil(total_rows / batch_size)

    def process_batch(batch_index):
    # offset = (batch_index * batch_size)
        offset = (batch_index * batch_size)
        cur.execute(f"SELECT {recipe_name}, {ingredient_name}, recipeid FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        # cur.execute(f"SELECT name, recipeid FROM {table_name}")
        results = cur.fetchall()
        texts = [result[0] for result in results]
        ingre = [result[1] for result in results]
        ids = [result[2] for result in results]
        if(len(ids) > 0 ):
            inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            inputs1 = tokenizer(ingre, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
                outputs1 = model(**inputs1)
                embeddings1 = outputs1.last_hidden_state.mean(dim=1).numpy()
            vectors = [(ids[i], embeddings[i]) for i in range(len(ids))]
            vectors1 = [(ids[i], embeddings1[i]) for i in range(len(ids))]
            print(f"Uploading vectors for batch {batch_index + 1}..")
            retry = 15
            retryIndicator = True
            while retry > 0 and retryIndicator:
                try :
                    res = index.upsert(vectors=vectors, namespace=namespace_name1)
                    res1 = index.upsert(vectors=vectors1, namespace=namespace_name2)
                    print(res)
                    print(res1)
                    retryIndicator = False
                except Exception as e: 
                    print( 'error in upsert retry for '+ namespace_name1 + 'or' + namespace_name2 + "   ---> " + str(e) )
                    time.sleep(5)
                    retry -=1
                    print('error in' +  str(retry))

    # Use ThreadPoolExecutor to process batches concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_batch, i) for i in range(num_batches)]
        if(len(futures)!=0):
            for future in concurrent.futures.as_completed(futures):
                future.result()

    # Close Snowflake connection
    cur.close()
    conn.close()

def upload_embeddings2pinecone2():

    # Create or retrieve a namespace in Pinecone
    namespace_name = 'ingredients_airflow'
    index_name = os.getenv('PINECONE_INDEX_NAME')
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    # Check whether the index with the same name already exists - if so, delete it
    if index_name not in pinecone.list_indexes().names():
        pinecone.create_index(name=index_name, dimension=768, spec=PodSpec(environment="gcp-starter"))
    index = pinecone.Index(name=index_name)

    # Load the DistilBERT model and tokenizer
    model_name = 'distilbert-base-uncased'
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name)

    # Snowflake connection parameters
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
    snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

    # Cursor to execute SQL queries
    cur = conn.cursor()
    table_name = os.getenv('TABLE_NAME')

    # Get the total number of rows in the table
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cur.fetchone()[0]
    # total_rows = 100000

    # Define the batch size
    batch_size = 100

    # Calculate the number of batches needed
    num_batches = math.ceil(total_rows / batch_size)

    def process_batch(batch_index):
        offset = (batch_index * batch_size)
        cur.execute(f"SELECT recipeingredientparts, recipeid FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
        results = cur.fetchall()
        texts = [result[0] for result in results]
        ids = [result[1] for result in results]
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
        vectors = [(ids[i], embeddings[i]) for i in range(len(ids))]
        print(f"Uploading vectors for batch {batch_index + 1}..")
        retry = 15
        retryIndicator = True
        while retry > 0 and retryIndicator :
            try :
                res = index.upsert(vectors=vectors, namespace=namespace_name)
                print(res)
                retryIndicator = False
            except Exception as e: 
                print( 'error in upsert retry for '+ namespace_name + "   ---> " + str(e) )
                time.sleep(5)
                retry -=1
                print('error in' +  str(retry))

    # Use ThreadPoolExecutor to process batches concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_batch, i) for i in range(num_batches)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Close Snowflake connection
    cur.close()
    conn.close()

##### TryE


dag = DAG(
    dag_id="sandbox",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["nutribuddy", "damg7245"],
)
    

with dag:
    start = BashOperator(
        task_id = "start",
        bash_command = 'echo "Triggering airflow pipeline!!"'
    )

    upload_csv2gcp_main = PythonOperator(
        task_id = 'Upload_to_GCP_main_block',
        python_callable = upload_csv2gcp_main,
        provide_context = True,
        dag = dag,
    )
    
    upload_gcp2snowflake_main = PythonOperator(
        task_id = 'Upload_from_GCP_to_Snowflake',
        python_callable = upload_gcp2snowflake_main,
        provide_context = True,
        dag = dag,
    )
    
    upload_recipeName2pinecone = PythonOperator(
        task_id='Upload_to_Pinecone_Recipe_Name_namespace',
        python_callable=upload_embeddings2pinecone_test,
        provide_context=True,
        # op_args = ['recipe_name_airflow','name'],
        op_args = ['recipe_name_3T200','name'],
        dag=dag,
    )

    upload_ingredients2pinecone = PythonOperator(
        task_id='Upload_to_Pinecone_Ingredient_namespace',
        python_callable=upload_embeddings2pinecone_test,
        provide_context=True,
        # op_args = ['recipe_name_airflow','name'],
        op_args = ['ingredients_3T200','recipeingredientparts'],
        dag=dag,
    )

    # upload_recipeName2pinecone = PythonOperator(
    #     task_id='Upload_to_Pinecone_Recipe_Name_namespace',
    #     python_callable=upload_embeddings2pinecone2,
    #     provide_context=True,
    #     # op_args = ['recipe_name_airflow','ingredients_airflow','name','recipeingredientparts'],
    #     dag=dag,
    # )
    
    # upload_ingredients2pinecone = PythonOperator(
    #     task_id='Upload_to_Pinecone_Ingredient_Name_namespace',
    #     python_callable=upload_embeddings2pinecone,
    #     provide_context=True,
    #     op_args = ['ingredients_airflow_test','recipeingredientparts'],
    #     dag=dag,
    # )


    start >> upload_csv2gcp_main >> upload_gcp2snowflake_main >> upload_recipeName2pinecone >> upload_ingredients2pinecone
    # start >> upload_csv2gcp_main >> upload_gcp2snowflake_main >> upload_recipeName2pinecone

