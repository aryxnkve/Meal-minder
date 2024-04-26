from sqlalchemy import Boolean, Column, Integer, String

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import sys


SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
TABLE_NAME = os.getenv("TABLE_NAME")

def connectionToSnow(connection_test=False):
    # load_dotenv(path,override=True)
    # user, password, _, account_identifier,_ = loadenv()
    engine = create_engine(
        'snowflake://{user}:{password}@{account_identifier}/'.format(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account_identifier=SNOWFLAKE_ACCOUNT,
        ), connect_args={'client_session_keep_alive': True}
    )
    try:
        connection = engine.connect()
        results = connection.execute('select current_version()').fetchone()
        print(results[0])
        if connection_test:
            connection.close()
        else:
            return connection
    finally:
        engine.dispose()

connection = connectionToSnow()

def get_recipe_data(id_list):
    query = f"SELECT recipeid, name, recipeingredientparts, recipeinstructions, calories FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{TABLE_NAME} WHERE recipeid IN ({id_list});"
    res = connection.execute(query).fetchall()
    results = []
    for r in res:
        row = []
        for col in r:
            row.append(col)
        results.append(row)
    # print(results)
    return results
