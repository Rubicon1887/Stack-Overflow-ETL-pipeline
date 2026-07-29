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
    day0=datetime.now(timezone.utc).date()-timedelta(days=1) # yesterday

    qs=fetch_1days_questions(tag,day0)
    filepath=save_raw_questions(qs,tag,day0)
    upload_to_s3(filepath,tag,day0)


    


if __name__=='__main__':
    fetch_save_upload()