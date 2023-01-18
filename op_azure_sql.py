from shared_helpers import query_azure_database
from shared_constants import API_FIELDS

# Create table
def create_azure_sql_table(table_name, environment):

    db_columns = [f'[{field}] [nvarchar](200) NULL' for field in API_FIELDS]
    
    columns_string = ','.join(db_columns)
    
    sql = f"""
        CREATE TABLE [dbo].[stg_{table_name}] (
            {columns_string}
        )
    """

    query_azure_database(sql,environment)

# Check if table exists


create_azure_sql_table('libcal_bookings_test')
