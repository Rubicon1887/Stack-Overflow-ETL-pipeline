from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone,date
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import boto3

import sys
sys.path.append('./')

from primary.pipeline import StackOverflowPipeline

def fetch_save_upload():

    languages=['python','java','javascript','typescript','c#']
    yesterday=datetime.now(timezone.utc).date()-timedelta(days=1)

    pipeline=StackOverflowPipeline()

    for lang in languages:

        print(colored(f'1 - Fetching Stack Overflow questions from {yesterday} tagged with {lang}','yellow'))
        qs=pipeline.fetch_1days_questions(day0=yesterday,lang=lang)
        print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

        # filepath=pipeline.save_raw_questions(day0=yesterday,lang=lang,qs=qs)
        # print(colored(f'3 - Saved {yesterday} data to {filepath}','blue'))

        json_data=json.dumps(qs,indent=2).encode('utf-8')

        bucket_name,key=pipeline.upload_to_S3(day0=yesterday,lang=lang,file=json_data)
        print(colored(f'4 - Uploaded raw {yesterday} file to s3://{bucket_name}/{key}','magenta'))

        # Here, I want to load questions from qs['items'] to postgres
        print(colored(f'5 - Loading rows to postgres','cyan'))
        pipeline.load_to_db(day0=yesterday,lang=lang,qs=qs['items'])
        print(colored(f'6 - Successfully loaded {len(qs['items'])}  {lang} rows to postgres','blue'))


if __name__=='__main__':
    fetch_save_upload()


# TODO: rename qs variable to better represent that it is the whole JSON payload, and not just the list of questions
# This script gets turned into a DAG so we can benefit from Airflow instead of the DAG calling only daily.py

I have an ELT pipeline that extracts data from an API, loads it to S3 and postgres running in a Docker container. The functionality and logic and functions are in a module pipeline.py and a script called daily.py calls 
those functions. A rough layout of daily.py is - 

languages=['python','java','c#','javascript','typescript']
pipeline=StackOverflowPipeline()

for lang in languages:
    qs=pipeline.fetch_questions(lang)
    pipeline.upload_to_S3(lang,qs)
    pipeline.upload_to_postgres(lang,qs)

How do I use Airflow to orchestrate this? I'd like to stick with the Taskflow paradigm. Is it a good idea to use Airflow through Docker? pipeline.py is in a folder "primary" inside my project folder
"Stack Overflow ELT pipeline". daily.py is in a folder "scripts". In the project folder, there is also a folder named "docker" which has the docker-compose.yml file for postgres. I understand that it is a
good idea to rewrite daily.py as an Airflow dag.