import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

host = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

def query_database(sql_statement, return_data=False):

    try :
        data_to_return = True
        conn = psycopg2.connect(host=host,dbname=dbname, user=user, password=password)
        cur = conn.cursor()
        cur.execute(sql_statement)
        if return_data:
            data_to_return = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return data_to_return

    except Exception as e:
        print(f'Could not complete sql query. Here is the exception returned: {e}')
        return False

# sql_statement = """
# select  *
# from public.slv_data
# where project = 'libcal'
# LIMIT 1000
# """

# print(query_database(sql_statement))