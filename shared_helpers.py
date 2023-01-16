import os
import csv

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
        # Not every call to the DB will require data to be returned by the function, hence the return_data flag
        if return_data:
            data_to_return = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return data_to_return

    except Exception as e:
        print(f'Could not complete sql query. Here is the exception returned: {e}')
        return False

def get_most_recent_date_in_db():
    sql_statement = """
        select date
        from public.slv_data
        where project = 'libcal'
        ORDER BY date DESC
        LIMIT 1
    """
    top_date_in_db = query_database(sql_statement, return_data=True)
    if not top_date_in_db:
        return False
        
    return top_date_in_db[0][0]

def export_to_csv(filename,data_to_write):

    f = open(f'{filename}.csv',"a+", newline='')

    with f:
        write = csv.writer(f)
        write.writerows(data_to_write)
