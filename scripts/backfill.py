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

    tag='python'
    start_date=date(2026,7,5)
    end_date=date(2026,7,10) # inclusive

    current=start_date
    while current<=end_date:

        extractor=Extract(current,tag)
        qs=extractor.fetch_1days_questions()
        filepath=extractor.save_raw_questions(qs)
        extractor.upload_to_s3(filepath)

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()