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
    start_date=date(2014,5,29)
    end_date=date(2014,12,31) # inclusive

    extractor=Extract(backfill=True)

    current=start_date
    while current<=end_date:

        for tag in tags:
            qs=extractor.fetch_1days_questions(current,tag)
            filepath=extractor.save_raw_questions(current,tag,qs)
            extractor.upload_to_S3(current,tag,filepath)

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()