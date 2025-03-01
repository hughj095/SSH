import pandas as pd
import json
from azure.cosmos import CosmosClient
import uuid

database_name = "ToDoList"
container_name = "GDP2024"
cosmos_db_uri = "https://cosmos-db-john.documents.azure.com:443/"
key = 'c7vSBJFfFcqjLnPix7Sll1kDrr0KLiof6BWEcRaskr7Hf9446t6OeKFtlMdM1QyDgVLHsvqHvE54ACDbou4uiQ=='


df = pd.read_csv("GDP_data_2024.csv")
df.to_json("data.json", orient="records")

client = CosmosClient(cosmos_db_uri, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
with open("data.json") as f:
    data = json.load(f)
    data = {
        "id": container_name,
        "data": data
    }
    container.create_item(body=data)

