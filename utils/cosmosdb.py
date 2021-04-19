execfile("configs/cosmosdb_config.py")

from azure.cosmos import CosmosClient
import uuid

def get_database_client():
  endpoint = cosmosdb_config['domain']
  key = cosmosdb_config['primary_key']
  client = CosmosClient(endpoint, credential=key)
  database_name = cosmosdb_config['database']
  database_client = client.get_database_client(database_name)

  return database_client

def get_refresh_token_cosmosdb_client():
  database_client = get_database_client()

  container_name = cosmosdb_config['refresh_token_container']
  container_client = database_client.get_container_client(container_name)

  return container_client

def get_access_token_cosmosdb_client():
  database_client = get_database_client()

  container_name = cosmosdb_config['access_token_container']
  container_client = database_client.get_container_client(container_name)

  return container_client

def get_access_token(exchange):
  access_token_client = get_access_token_cosmosdb_client()

  previous_access_token_expired = True
  token = None
  for item in access_token_client.query_items(query='SELECT * FROM c WHERE c.exchange = "%s"' % (exchange)):
    previous_access_token_expired = False
    token = item

  if not previous_access_token_expired:
    return token

  refresh_token_client = get_refresh_token_cosmosdb_client()
  for item in refresh_token_client.query_items(query='SELECT * FROM c WHERE c.exchange = "%s"' % (exchange)):
    token = item

  return token

def add_new_access_token(exchange, new_access_token):
  access_token_client = get_access_token_cosmosdb_client()

  access_token_client.upsert_item({
      'id': str(uuid.uuid4()),
      'exchange': exchange,
      'access_token': new_access_token['access_token'],
      'api_server': new_access_token['api_server'],
      'token_type': new_access_token['token_type']
    }
  )

def update_to_new_refresh_token(exchange, new_access_token):
  refresh_token_client = get_refresh_token_cosmosdb_client()

  token = None
  for item in refresh_token_client.query_items(query='SELECT * FROM c WHERE c.exchange = "%s"' % (exchange)):
    token = item

  refresh_token_client.upsert_item({
      'id': token['id'],
      'exchange': token['exchange'],
      'refresh_token': new_access_token['refresh_token'],
      'token_type': new_access_token['token_type']
    }
  )
