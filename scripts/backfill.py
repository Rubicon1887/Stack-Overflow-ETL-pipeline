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

    # tags=['python','java','javascript','typescript','c#']
    tag='python'
    start_date=date(2026,6,1)
    end_date=date(2026,6,30) # inclusive

    extractor=Extract(tag,backfill=True)

    current=start_date
    while current<=end_date:
    
        qs=extractor.fetch_1days_questions(current)
        # filepath=extractor.save_raw_questions(qs)
        # extractor.upload_to_s3(filepath)

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()