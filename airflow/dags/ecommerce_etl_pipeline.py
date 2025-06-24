import boto3
import pandas as pd
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# S3 Configuration
S3_BUCKET_NAME = 'my-ecommerce-data-bucketkt'  # Your S3 Bucket
S3_RAW_PATH = 'raw_data/'  # Folder in S3 for raw files
S3_PROCESSED_PATH = 'processed_data/'  # Folder in S3 for processed files

# Set up AWS S3 Client using boto3
s3_client = boto3.client('s3', region_name='eu-north-1')

# Define paths for EC2 instance
PROCESSED_PATH = '/home/ubuntu/airflow/data/processed'

# Define transformation function
def transform_data():
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # Download files from S3
    s3_client.download_file(S3_BUCKET_NAME, f"{S3_RAW_PATH}/customers.csv", "/tmp/customers.csv")
    s3_client.download_file(S3_BUCKET_NAME, f"{S3_RAW_PATH}/products.csv", "/tmp/products.csv")
    s3_client.download_file(S3_BUCKET_NAME, f"{S3_RAW_PATH}/orders.csv", "/tmp/orders.csv")

    # Load raw CSVs
    customers = pd.read_csv("/tmp/customers.csv")
    products = pd.read_csv("/tmp/products.csv")
    orders = pd.read_csv("/tmp/orders.csv")

    # Join all tables
    merged = orders.merge(customers, on='customer_id').merge(products, on='product_id')

    # Rename name_x and name_y to meaningful names
    merged.rename(columns={
        'name_x': 'customer_name',
        'name_y': 'product_name'
    }, inplace=True)

    # Add metrics
    merged['total_price'] = merged['quantity'] * merged['selling_price']
    merged['shipping_time_days'] = (
        pd.to_datetime(merged['delivery_date']) - pd.to_datetime(merged['order_date'])
    ).dt.days

    # Select relevant columns
    output = merged[[ 
        'order_id', 'customer_id', 'customer_name', 'email', 'country', 
        'product_id', 'category', 'selling_price', 'quantity', 
        'total_price', 'order_date', 'delivery_date', 'shipping_time_days'
    ]]

    # Save to local file (processed data on EC2)
    output_file = f"{PROCESSED_PATH}/final_output.csv"
    output.to_csv(output_file, index=False)
    print(f"✅ Data transformed and saved locally as {output_file}")

    # Upload the processed file back to S3
    upload_to_s3(output_file)

def upload_to_s3(local_file_path):
    # Upload file to S3
    file_name = os.path.basename(local_file_path)
    s3_file_path = f"{S3_PROCESSED_PATH}{file_name}"

    try:
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, s3_file_path)
        print(f"✅ Successfully uploaded {file_name} to S3 at {S3_BUCKET_NAME}/{s3_file_path}")
    except Exception as e:
        print(f"❌ Failed to upload {file_name} to S3: {str(e)}")

# Default args for DAG
default_args = {
    'owner': 'kartavya',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define DAG
with DAG(
    dag_id='ecommerce_etl_pipeline_s3',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',  # or None for manual triggering
    catchup=False
) as dag:

    transform = PythonOperator(
        task_id='transform_ecommerce_data',
        python_callable=transform_data
    )

    transform

# Make sure to include the DAG in the globals() to register it
globals()['dag'] = dag
