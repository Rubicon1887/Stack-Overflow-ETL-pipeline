import pendulum
from datetime import datetime
from airflow.sdk import dag,task

import sys
sys.path.append('./')

from primary.pipeline import StackOverflowPipeline

@dag(
    dag_id='daily_dag',
    schedule='daily',
    start_date=
)