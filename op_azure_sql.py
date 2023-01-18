from shared_helpers import query_azure_database
from shared_constants import API_FIELDS, DB_TABLE_NAME

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
