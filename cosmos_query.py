from azure.cosmos import CosmosClient
import pandas as pd

# Replace these with your actual Azure Cosmos DB credentials
ENDPOINT = "https://cosmos-db-john.documents.azure.com:443/"
KEY = "c7vSBJFfFcqjLnPix7Sll1kDrr0KLiof6BWEcRaskr7Hf9446t6OeKFtlMdM1QyDgVLHsvqHvE54ACDbou4uiQ=="
DATABASE_NAME = "ToDoList"
CONTAINER_NAME = "GDP2024"
JSON_COL_HEADER = "data"

# Initialize the Cosmos client
client = CosmosClient(ENDPOINT, KEY)

# Get the database and container
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

# Define SQL query
query = f"SELECT c.{JSON_COL_HEADER} FROM c"

# Execute query and fetch results
items = list(container.query_items(query=query, enable_cross_partition_query=True))

# Parse and df and sort
df = pd.DataFrame(items[0]['data'])
df = df.sort_values(by='Q3', ascending=False, ignore_index=True)

# Print DataFrame
print(df)
