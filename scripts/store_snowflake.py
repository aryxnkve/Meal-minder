# pip install pandas
from google.cloud import storage
import pandas as pd
import snowflake.connector
import io
import os
from dotenv import load_dotenv

env_path = 'C:/Users/aptea/OneDrive/Documents/NEU/Sem6/BDIA/NutriBuddy/scripts/.env'
load_dotenv(dotenv_path=env_path)

def get_snowflake_data_type(dtype):
    # Example mapping, adjust as needed
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


# Access the CSV file in the GCP bucket
bucket_name = os.getenv('BUCKET_NAME')
blob_name = os.getenv('BLOB_NAME')
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# Read the CSV data as a file-like object
csv_data = io.BytesIO(blob.download_as_string())

# Load the CSV data into a DataFrame
df = pd.read_csv(csv_data)

# Set up Snowflake connection parameters
snowflake_user = os.getenv('SNOWFLAKE_USER')
snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
snowflake_warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')

conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)

cur = conn.cursor()

# Generate the CREATE TABLE statement based on DataFrame columns and data types
table_name = os.getenv('TABLE_NAME')
create_table_sql = "CREATE OR REPLACE TABLE " + table_name + "("
for column_name, dtype in zip(df.columns, df.dtypes):
    snowflake_dtype = get_snowflake_data_type(dtype)
    create_table_sql += f"{column_name} {snowflake_dtype}, "
create_table_sql = create_table_sql[:-2] + ")"  # Remove the trailing comma and space, add closing parenthesis

# Execute the CREATE TABLE statement
cur.execute(create_table_sql)

# Generate the INSERT INTO statement
insert_into_sql = f"INSERT INTO " + table_name + f"({', '.join(df.columns)}) VALUES ({', '.join(['%s']*len(df.columns))})"

# Execute the INSERT INTO statement
cur.executemany(insert_into_sql, df.values.tolist())


# Commit the transaction
conn.commit()

# Close Snowflake connection
cur.close()
conn.close()