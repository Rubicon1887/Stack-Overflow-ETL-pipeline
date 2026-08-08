import boto3
from datetime import date
from dotenv import load_dotenv
import os
import json

load_dotenv()

client=boto3.client('s3')
tags=['python','java','javascript','typescript','c#']

def load_to_db():

    start_date=date(2021,8,18)
    # end_date=date(2016,12,31)
    end_date=date(2021,8,19)

    current=start_date
    while current<=end_date:
        for tag in tags:

            key=(
                f'raw/'
                f'{current.year}/'
                f'{current.month:02d}/'
                f'{current.day:02d}/'
                f'{tag}_questions.json'
            )

            obj=client.get_object(Bucket=os.getenv('S3_BUCKET_NAME',Key=key))
            data=obj['Body'].read().decode('utf-8')
            qs=json.loads(data)['items']

            question_id bigint NOT NULL,
                    programming_language varchar NULL,
                    tags _varchar NULL,
                    owner_id bigint NULL,
                    owner_reputation bigint NULL,
                    owner_name varchar NULL,
                    is_answered boolean NULL,
                    view_count bigint NULL,
                    closed_date bigint NULL,
                    answer_count bigint NULL,
                    score bigint NULL,
                    question_date date NULL,