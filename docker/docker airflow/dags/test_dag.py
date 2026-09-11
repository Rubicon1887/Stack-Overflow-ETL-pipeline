from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="test_dag",
    start_date=datetime(2021, 1, 1),
    schedule="* * * * *",   # runs every minute
    catchup=False,
)
def taskflow_chain():
    
    @task
    def extract():
        return "Hello from extract"

    @task
    def transform(msg: str):
        return msg.upper()

    @task
    def load(msg: str):
        print(f"Loaded message: {msg}")

    load(transform(extract()))

dag = taskflow_chain()
