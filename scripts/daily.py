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
        print(colored(f'4 - Uploaded {yesterday} file to s3://{bucket_name}/{key}','magenta'))

        # Here, I want to load questions from qs['items'] to postgres
        print(colored(f'5 - Loading rows to postgres','cyan'))
        pipeline.load_to_db(day0=yesterday,lang=lang,qs=qs['items'])
        print(colored(f'6 - Successfully loaded {len(qs['items'])} to postgres','blue'))


if __name__=='__main__':
    fetch_save_upload()