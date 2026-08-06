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
    with open(r'scripts\stop_date.txt','r') as f:
        start_date=date.fromisoformat(f.read())
    end_date=date(2020,12,31) # inclusive

    # start_date=date(2026,8,1)
    # end_date=date(2026,8,2)

    extractor=Extract()

    print(colored(f'Starting backfill at {start_date}.','yellow'))
    current=start_date
    while current<=end_date:

        for tag in tags:
            qs=extractor.fetch_1days_questions(current,tag)
            # filepath=extractor.save_raw_questions(current,tag,qs)
            json_data=json.dumps(qs,indent=2).encode('utf-8')
            extractor.upload_to_S3(current,tag,json_data)

        if qs['quota_remaining']<300:

            with open(r'scripts\stop_date.txt','w') as f:
                f.write(current.isoformat())
            print(colored(f'Stopping backfill at {current}. Quota remaining - {qs['quota_remaining']}','red'))

            break

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()

# TODO: pass arguments as keyowrd argments for readability