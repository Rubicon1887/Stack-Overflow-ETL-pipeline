from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import boto3

load_dotenv()

api_key=os.getenv('STACK_API_KEY')
bucket_name=os.getenv('S3_BUCKET_NAME')

def fetch_yesterdays_questions(tags):
    
    SITE=StackAPI('stackoverflow',key=api_key)
    SITE.page_size=100
    SITE.max_pages=15

    today=datetime.now(timezone.utc).date()
    yesterday=today-timedelta(days=1)

    fromdate=int(datetime.combine(yesterday,time.min,tzinfo=timezone.utc).timestamp())
    todate=int(datetime.combine(today,time.min,tzinfo=timezone.utc).timestamp())

    print(colored(f'1 - Fetching Stack Overflow questions from {yesterday} tagged with {tags}','yellow'))
    qs=SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=tags)
    print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

    return qs

def save_raw_questions(qs,tags):

    now=datetime.now()
    path=Path(
        r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
        f'{now.year}',
        f'{now.month:02d}',
        f'{now.day:02d}'
    )

    path.mkdir(parents=True,exist_ok=True)
    filepath=path/f'{tags}_questions.json'

    with open(filepath,'w',encoding='utf-8') as f:
        json.dump(qs,f,indent=2)
    print(colored(f'3 - Saved {now.date()} data to {filepath}','blue'))

    return filepath

def upload_to_s3(filepath,tags):

    client=boto3.client('s3')
    now=datetime.now()

    key=(
        f'raw/'
        f'{now.year}/'
        f'{now.month:02d}/'
        f'{now.day:02d}/'
        f'{tags}_questions.json'
    )

    client.upload_file(filepath,bucket_name,key)
    print(colored(f'4 - Uploaded {now.date()} file to s3://{bucket_name}/{key}','magenta'))

def fetch_save_upload():

    tags='python'

    qs=fetch_yesterdays_questions(tags)
    filepath=save_raw_questions(qs,tags)
    upload_to_s3(filepath,tags)


if __name__=='__main__':
    fetch_save_upload()