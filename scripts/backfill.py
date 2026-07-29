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

from primary.extract import fetch_1days_questions,save_raw_questions,upload_to_s3
from primary.extract import extract

def fetch_save_upload():

    tag='python'
    start_date=date(2026,7,5)
    end_date=date(2026,7,10) # inclusive

    current=start_date
    while current<=end_date:

        self=extract(current)
        qs=self.fetch_1days_questions(tag)
        filepath=self.save_raw_questions(qs,tag)
        self.upload_to_s3(filepath,tag)

        current+=timedelta(days=1)


if __name__=='__main__':
    fetch_save_upload()