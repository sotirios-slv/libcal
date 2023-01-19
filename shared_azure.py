from datetime import datetime, date
import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
from dotenv import load_dotenv

from shared_constants import API_FIELDS, AZURE_VARIABLES, EARLIEST_DATE, DB_TABLE_NAME

load_dotenv()
azure_client_id = os.environ.get('AZURE_CLIENT_ID')
azure_client_secret = os.environ.get('AZURE_CLIENT_SECRET')
azure_tenant_id = os.environ.get('AZURE_TENANT_ID')
subscription_id = os.environ.get('AZURE_DEV_SUB_ID')


def get_key_vault_secret(secret_to_retrieve, vault_url):

    credentials = ClientSecretCredential(client_id=azure_client_id, client_secret=azure_client_secret,tenant_id=azure_tenant_id)
    client = SecretClient(credential=credentials, vault_url=vault_url)

    sql_connection_string = client.get_secret(secret_to_retrieve)

    if not sql_connection_string.value:
        print('Unable to retrieve key vault secret')
        return False

    return sql_connection_string.value

def check_if_table_exists(environment,prepend=False):

    table_name = DB_TABLE_NAME
    if prepend:
        table_name = f'{prepend}_{table_name}'

    sql = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'dbo'
        AND TABLE_NAME = '{table_name}';
    """
    res = query_azure_database(sql, environment, return_data=True)

    if len(res) == 0:
        return False

    return True

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

def create_azure_sql_table(environment, prepend=False ):

    db_columns = [f'[{field}] [nvarchar](200) NULL' for field in API_FIELDS]
    
    table_name = DB_TABLE_NAME
    if prepend:
        table_name = f'{prepend}_{table_name}'

    columns_string = ','.join(db_columns)
    
    sql = f"""
        CREATE TABLE [dbo].[{table_name}] (
            {columns_string}
        )
    """
    query_azure_database(sql,environment)

def get_most_recent_date_in_db(environment, prepend=False):

    if check_if_table_exists(environment,prepend=prepend) == False:
        return datetime.strptime(EARLIEST_DATE,'%Y-%m-%d').date()

    table_name = DB_TABLE_NAME
    if prepend:
        table_name = f'{prepend}_{DB_TABLE_NAME}'

    sql_statement = f"""
        SELECT TOP (1) [fromDate]
        FROM [dbo].[{table_name}]
        ORDER BY [fromDate] DESC
    """
    top_date_in_db = query_azure_database(sql_statement, environment=environment, return_data=True)

    if not top_date_in_db:
        return datetime.strptime(EARLIEST_DATE,'%Y-%m-%d').date()

    return datetime.strptime(top_date_in_db[0][0],'%Y-%m-%d').date()

# print(get_most_recent_date_in_db('dev',prepend='stg'))