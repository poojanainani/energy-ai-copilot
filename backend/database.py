import pandas as pd
import psycopg2


def run_query(sql):

    conn = psycopg2.connect(
        host="localhost",
        database="energy_project",
        user="postgres",
        password="Summer@123"
    )

    try:
        return pd.read_sql_query(sql, conn)

    finally:
        conn.close()