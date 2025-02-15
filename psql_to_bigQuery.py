import os
import pandas as pd
from sqlalchemy import create_engine
from google.cloud import storage, bigquery

# PostgreSQL Connection Details
POSTGRES_HOST = "4.246.225.136"
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "4rfv5tgb^YHN&UJM"
POSTGRES_PORT = "5432"  # Change if different
table_name = "test"

# Google Cloud Details
GCS_BUCKET_NAME = "vmjohn3_gcpbucket"
BIGQUERY_PROJECT = "bq-project1-451012"
BIGQUERY_DATASET = "dataset_bq1"

# Set Google Cloud Credentials
#service_account = svc_vmjohn3
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\johnm\OneDrive\Desktop\SSH\bq-project1-451012-641dc9bc0a5d.json"

def extract_postgres_table(table_name):
    """Extracts a PostgreSQL table and returns a DataFrame."""
    engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

def upload_to_gcs(df, table_name):
    """Uploads a DataFrame as a CSV to Google Cloud Storage."""
    csv_filename = f"{table_name}.csv"
    df.to_csv(csv_filename, index=False)
    
    client = storage.Client(project="bq-project1-451012")
    print(GCS_BUCKET_NAME)
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(f"{table_name}.csv")
    blob.upload_from_filename(csv_filename)
    
    print(f"Uploaded {csv_filename} to gs://{GCS_BUCKET_NAME}/{table_name}.csv")

def load_into_bigquery(table_name):
    """Loads the CSV from GCS into BigQuery."""
    client = bigquery.Client()
    table_id = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )

    uri = f"gs://{GCS_BUCKET_NAME}/{table_name}.csv"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Wait for the job to complete
    
    print(f"Loaded data into BigQuery table {table_id}")

def main(table_name):
    tables = [table_name]
    for table in tables:
        df = extract_postgres_table(table)
        upload_to_gcs(df, table)
        load_into_bigquery(table)
    
    print("PostgreSQL data successfully copied to BigQuery!")

if __name__ == "__main__":
    main(table_name)
