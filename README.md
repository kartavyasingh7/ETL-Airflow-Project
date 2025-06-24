
# **E-Commerce ETL Pipeline with AWS S3 Integration**

## **Overview**
This project automates the **ETL (Extract, Transform, Load)** process for e-commerce data, transforming raw customer, product, and order data into meaningful analytics. The pipeline is designed to run on **Apache Airflow** and uses **AWS S3** for cloud-based storage. The system automatically downloads raw data from an S3 bucket, processes it, and uploads the transformed data back to S3.

---

## **Key Features**
- **Automated Data Processing**: The pipeline automates the extraction of raw data from AWS S3, performs transformations, and loads the processed data back into S3.
- **Cloud-Based Architecture**: The project is designed to run on an **AWS EC2** instance, leveraging **AWS S3** for storage.
- **Scalable and Robust**: Using **Apache Airflow** for scheduling and task management, the pipeline is highly scalable and fault-tolerant.
- **Data Transformation**: Data from multiple sources is merged, and key metrics like `total_price` and `shipping_time_days` are calculated.
- **Error Handling**: The pipeline is equipped with retry mechanisms for task failures, making it reliable for production environments.
- **Security**: AWS IAM roles and credentials are securely managed.

---

## **Tech Stack**
- **Apache Airflow**: For orchestrating and automating the data pipeline.
- **AWS S3**: For storing raw and processed data.
- **Python**: Main programming language for writing transformation logic.
- **Boto3**: AWS SDK for Python, enabling interaction with AWS S3.
- **Pandas**: For data manipulation and transformation.
- **IAM**: To manage permissions for secure access to S3.
- **Ubuntu**: The EC2 instance runs on Ubuntu, ensuring compatibility with the Airflow environment.

---

## **Project Structure**
```bash
/airflow
├── dags
│   ├── ecommerce_etl_pipeline.py  # Main Airflow DAG for ETL process
│
├── data
│   ├── raw  # Raw data folder (not used in this version)
│   ├── processed  # Processed data folder (used in EC2)
│
└── requirements.txt  # List of dependencies
```

---

## **Getting Started**

### **Prerequisites**
1. **AWS Account**: Ensure you have an AWS account with permissions to access EC2, S3, and IAM roles.
2. **Airflow Setup**: Set up **Apache Airflow** on an EC2 instance (or local machine).
3. **S3 Bucket**: Create an S3 bucket for raw and processed data storage.

### **Steps to Run the Project**

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/ecommerce-etl-pipeline.git
    cd ecommerce-etl-pipeline
    ```

2. **Set Up Python Environment**
    Install dependencies using `pip`:
    ```bash
    python3 -m venv airflow_env
    source airflow_env/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure AWS Credentials**
   - Set your AWS credentials on the EC2 instance or in your local environment.
   - Alternatively, use **IAM Roles** for secure access management in AWS.

4. **Update S3 Bucket and Paths**
   Modify the `S3_BUCKET_NAME`, `S3_RAW_PATH`, and `S3_PROCESSED_PATH` variables in the script:
   ```python
   S3_BUCKET_NAME = 'your-bucket-name'
   S3_RAW_PATH = 'raw_data/'
   S3_PROCESSED_PATH = 'processed_data/'
   ```

5. **Start Airflow Scheduler**
   Run the following commands on your EC2 instance (or local environment):
   ```bash
   source ~/airflow_env/bin/activate
   airflow scheduler
   ```

6. **Monitor the Airflow Web UI**
   - Access the Airflow UI by navigating to `http://<EC2-IP>:8080` in your browser.
   - Start the **ecommerce_etl_pipeline_s3** DAG manually or wait for the scheduled run.

---

## **Airflow DAG Details**

### **DAG Tasks**
- **Download Raw Data**: Downloads CSV files from the specified S3 bucket.
- **Transform Data**: Merges raw data, performs data transformation (e.g., calculating `total_price`, `shipping_time_days`), and saves the output locally on the EC2 instance.
- **Upload Processed Data**: Uploads the processed data back to an S3 bucket for further use.

### **Retry Mechanism**
- The DAG is configured with a retry delay of **5 minutes** and will attempt retries **once** upon failure.

---

## **Data Transformation Logic**

1. **Merging Data**:
   - The raw datasets (customers, products, and orders) are merged based on customer and product IDs.

2. **Calculating Metrics**:
   - `total_price`: Calculated as `quantity * selling_price`.
   - `shipping_time_days`: Calculated as the difference between `delivery_date` and `order_date`.

3. **Final Data Selection**:
   - Only relevant columns are retained, including `order_id`, `customer_id`, `customer_name`, `email`, `product_name`, etc.

---

## **Security Considerations**
- **IAM Roles**: We’ve assigned **IAM roles** to the EC2 instance for secure access to S3. This avoids the need to use hardcoded AWS credentials.
- **Sensitive Data**: Never store sensitive information (e.g., AWS keys) in your codebase. Use **IAM roles** or **environment variables** to manage credentials.

---

## **Future Enhancements**
- **Scalability**: Transition from the **Sequential Executor** to the **Celery Executor** for parallel task execution.
- **Data Quality Assurance**: Integrate data validation steps to ensure the quality of the processed data.
- **Logging and Monitoring**: Implement detailed logging and monitoring using **AWS CloudWatch** or other third-party tools for real-time tracking and alerts.
- **Error Notifications**: Enhance the DAG to send notifications (e.g., email, Slack) when tasks fail.

---

## **License**
MIT License.
