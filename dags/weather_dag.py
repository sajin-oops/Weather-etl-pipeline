from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path so we can import our extract/transform/load modules
sys.path.insert(0, "/Users/sajina.k/weather-etl-pipeline")

from extract.fetch_weather import fetch_weather
from transform.transform_weather import transform_weather
from load.load_to_postgres import insert_weather


def run_etl():
    record = fetch_weather("London")
    record["recorded_at"] = datetime.fromtimestamp(record["recorded_at"])
    transformed = transform_weather(record)
    insert_weather(transformed)
    print("Weather ETL completed successfully!")


default_args = {
    "owner": "sajin",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    description="Fetch, transform, and load weather data hourly",
    schedule_interval="@seconds=5",
    start_date=datetime(2026, 7, 18),
    catchup=False,
    tags=["weather", "etl"],
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_weather_etl",
        python_callable=run_etl,
    )