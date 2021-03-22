import os
import psycopg2
import pandas as pd

config = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASS"),
    database=os.getenv("PG_DB"),
)


def execute_sql(sql):
    try:
        db = config
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)


def get_ncs(sql):
    try:
        db = config
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)


def get_df(sql):
    try:
        df = pd.read_sql_query(sql, config)
        return df
    except Exception as e:
        print(e)
