import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from dotenv import load_dotenv

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

