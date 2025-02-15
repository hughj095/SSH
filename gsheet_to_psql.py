import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Variables
csv_file_path = "https://docs.google.com/spreadsheets/d/1O_wI-ek5z8RQcjuJLr94jiwF1O7wHG5j4Q8DQJ3uDlI/export?format=csv"
db_host = "4.246.225.136"
db_port = "5432"  # Default PostgreSQL port
db_name = "postgres"
db_user = "postgres"
db_password = "4rfv5tgb^YHN&UJM"
table_name = "test"

# Read CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Create a connection to PostgreSQL using SQLAlchemy
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Save DataFrame to PostgreSQL table
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully inserted into {table_name}")
