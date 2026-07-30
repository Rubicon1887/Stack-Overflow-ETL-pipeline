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
    yesterday=datetime.now(timezone.utc).date()-timedelta(days=1)

    extractor=Extract(tag)
    qs=extractor.fetch_1days_questions(yesterday)
    filepath=extractor.save_raw_questions(yesterday,qs)
    extractor.upload_to_s3(yesterday,filepath)


if __name__=='__main__':
    fetch_save_upload()