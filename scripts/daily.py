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

from primary.extract import Extract

def fetch_save_upload():

    tags=['python','java','javascript','typescript','c#']
    yesterday=datetime.now(timezone.utc).date()-timedelta(days=1)

    extractor=Extract()

    for tag in tags:

        print(colored(f'1 - Fetching Stack Overflow questions from {yesterday} tagged with {tag}','yellow'))
        qs=extractor.fetch_1days_questions(yesterday,tag)
        print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

        # filepath=extractor.save_raw_questions(yesterday,tag,qs)
        # print(colored(f'3 - Saved {yesterday} data to {filepath}','blue'))

        json_data=json.dumps(qs,indent=2).encode('utf-8')

        bucket_name,key=extractor.upload_to_S3(yesterday,tag,json_data)
        print(colored(f'4 - Uploaded {yesterday} file to s3://{bucket_name}/{key}','magenta'))


if __name__=='__main__':
    fetch_save_upload()

# TODO: pass arguments as keyowrd argments for readability