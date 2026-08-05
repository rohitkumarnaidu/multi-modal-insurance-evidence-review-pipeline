# Cloud Orchestration Guide

To run the Multi-Modal Evidence Review pipeline in a production cloud environment, we recommend using a data orchestrator like **Apache Airflow**.

## Why Orchestrate?

- **Fault Tolerance**: If a node crashes, Airflow can retry the task.
- **Monitoring**: Visualize DAG execution, track success/failure rates, and alert on pipeline stalls.
- **Data Partitioning**: You can split a large 100,000-claim CSV into 1,000 chunks of 100 claims each, and run them in parallel Airflow workers.

## Sample Apache Airflow DAG

Below is a conceptual DAG for running this pipeline nightly.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'insurance_team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'evidence_review_pipeline',
    default_args=default_args,
    description='Nightly run of Multi-Modal Evidence Review',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # 1. Fetch claims from Data Warehouse to CSV
    fetch_data = BashOperator(
        task_id='fetch_claims_csv',
        bash_command='python scripts/export_bq_to_csv.py --dest dataset/claims.csv'
    )

    # 2. Run the main processing pipeline
    run_pipeline = BashOperator(
        task_id='run_evidence_review',
        bash_command='cd code && python main.py --parallel --workers 20'
    )

    # 3. Upload output to Data Warehouse
    upload_results = BashOperator(
        task_id='upload_results',
        bash_command='python scripts/import_csv_to_bq.py --src dataset/output.csv'
    )

    fetch_data >> run_pipeline >> upload_results
```

## Productionizing Images
The pipeline expects local file paths in `image_paths`. In production:
1. Ensure the upstream data extraction task (`fetch_claims_csv`) downloads the images from S3/GCS to local disk, OR
2. Modify `data_loader.py` and the Image Hash logic to directly read byte streams from your cloud blob storage using `boto3` or `google-cloud-storage`.
