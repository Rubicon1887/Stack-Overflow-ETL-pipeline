from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import boto3

load_dotenv()

api_key=os.getenv('STACK_API_KEY')
bucket_name=os.getenv('S3_BUCKET_NAME')

def fetch_day_questions(tags,day1,day0):
    
    SITE=StackAPI('stackoverflow')
    SITE.page_size=100
    SITE.max_pages=15

    fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
    todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

    print(colored(f'1 - Fetching Stack Overflow questions from {day0} tagged with {tags}','yellow'))
    qs=SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=tags)
    print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

    return qs