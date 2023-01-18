import os
import csv

from dotenv import load_dotenv
import psycopg2
import pyodbc

from shared_azure import get_key_vault_secret
from shared_constants import AZURE_VARIABLES

load_dotenv()

host = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')


def query_database(sql_statement, return_data=False):
    """helper function to run any valid SQL statement against the DB

    Args:
        sql_statement (string): SQL statement
        return_data (bool, optional): If set to true will return the data returned by the SQL query. Defaults to False.

    Returns:
        bool: Will return True/False flag to indicate that the SQL statement was successfully run
        list: Data returned from the database
    """
    try :
        data_to_return = True
        conn = psycopg2.connect(host=host,dbname=dbname, user=user, password=password)
        cur = conn.cursor()
        cur.execute(sql_statement)
        #* Not every call to the DB will require data to be returned by the function, hence the return_data flag
        if return_data:
            data_to_return = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return data_to_return

    except Exception as e:
        print(f'Could not complete sql query. Here is the exception returned: {e}')
        return False

def query_azure_database(sql_statement,environment='dev',return_data=False):

    username = get_key_vault_secret('sqladminuser',AZURE_VARIABLES[environment])
    password = get_key_vault_secret('sqladminpassword',AZURE_VARIABLES[environment])
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:slv-{environment}-sqldw.database.windows.net,1433;Database={environment}-edw;Uid={username};Pwd={{{password}}};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    try:
        data_to_return = True
        con = pyodbc.connect(connection_string)
        cursor = con.cursor()
        cursor.execute(sql_statement)
        if return_data:
            data_to_return = cursor.fetchall()
        con.commit()
        con.close()
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

def export_to_csv(filename,data_to_write,column_names):
    """Helper function to write any list to a CSV file

    Args:
        filename (string): The filename (without .csv file extension) to export the data to
        data_to_write (list): Data to add to the csv file, each item will be added to a new line 
        column_names (list): Column names to add to the first line of the csv file  
    """

    f = open(f'{filename}.csv',"a+", newline='')

    with f:
        write = csv.writer(f)
        write.writerow(column_names)
        write.writerows(data_to_write)