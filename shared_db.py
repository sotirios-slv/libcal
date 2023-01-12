import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

host = os.environ.get('HOST')
dbname = os.environ.get('DBNAME')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

def query_database(sql_statement):

    try :
        conn = psycopg2.connect(host=host,dbname=dbname, user=user, password=password)
        cur = conn.cursor()
        cur.execute(sql_statement)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f'Could not complete sql query. Here is the exception returned: {e}')
        return False
