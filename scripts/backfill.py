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
    with open(r'scripts\stop_date.txt','r') as f:
        start_date=date.fromisoformat(f.read())
    end_date=date(2020,12,31) # inclusive

    # start_date=date(2026,8,1)
    # end_date=date(2026,8,2)

    pipeline=StackOverflowPipeline()

    print(colored(f'Starting backfill at {start_date}.','yellow'))
    current=start_date
    while current<=end_date:
        for lang in languages:

            qs=pipeline.fetch_1days_questions(day0=current,lang=lang)
            # filepath=pipeline.save_raw_questions(day0=current,lang=lang,qs=qs)
            json_data=json.dumps(qs,indent=2).encode('utf-8')
            pipeline.upload_to_S3(day0=current,lang=lang,file=json_data)

        if qs['quota_remaining']<100:

            with open(r'scripts\stop_date.txt','w') as f:
                f.write(current.isoformat())
            print(colored(f'Stopping backfill at {current}. Quota remaining - {qs['quota_remaining']}','red'))

            break

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()

# TODO: pass arguments as keyowrd argments for readability