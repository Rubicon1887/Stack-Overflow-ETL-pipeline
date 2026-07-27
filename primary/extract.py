from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone,date
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import boto3

load_dotenv()

api_key=os.getenv('STACK_API_KEY')
bucket_name=os.getenv('S3_BUCKET_NAME')

SITE=StackAPI('stackoverflow',key=api_key)
SITE.page_size=100
SITE.max_pages=15

client=boto3.client('s3')

def fetch_1days_questions(tags,day0): # I want the choice between day 0 and yesterday to be made BEFORE these 3 methods are called, inside the driver code.

    day1=day0+timedelta(days=1)

    fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
    todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

    # if day1 is None and day0 is None: # yesterday's questions
        
    #     today=datetime.now(timezone.utc).date()
    #     yesterday=today-timedelta(days=1)

    #     fromdate=int(datetime.combine(yesterday,time.min,tzinfo=timezone.utc).timestamp())
    #     todate=int(datetime.combine(today,time.min,tzinfo=timezone.utc).timestamp())

    #     print(colored(f'1 - Fetching Stack Overflow questions from {yesterday} tagged with {tags}','yellow'))

    # elif day1 is not None and day0 is None: # questions for a day between data dump and yesterday

    #     fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
    #     todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

    #     print(colored(f'1 - Fetching Stack Overflow questions from {day0} tagged with {tags}','yellow'))

    # else:
    #     raise ValueError('Neither or both of day1 and day0 must be None')

    print(colored(f'1 - Fetching Stack Overflow questions from {day0} tagged with {tags}','yellow'))
    qs=SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=tags)
    print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

    return qs

def save_raw_questions(qs,tags,day0):

    path=Path(
        r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
        f'{day0.year}',
        f'{day0.month:02d}',
        f'{day0.day:02d}'
    )

    path.mkdir(parents=True,exist_ok=True)
    filepath=path/f'{tags}_questions.json'

    with open(filepath,'w',encoding='utf-8') as f:
        json.dump(qs,f,indent=2)
    print(colored(f'3 - Saved {day0} data to {filepath}','blue'))

    return filepath

def upload_to_s3(filepath,tags,day0):

    key=(
        f'raw/'
        f'{day0.year}/'
        f'{day0.month:02d}/'
        f'{day0.day:02d}/'
        f'{tags}_questions.json'
    )

    client.upload_file(filepath,bucket_name,key)
    print(colored(f'4 - Uploaded {day0} file to s3://{bucket_name}/{key}','magenta'))

def fetch_save_upload():

    tags='python'
    day0=datetime.now(timezone.utc).date() # or date(year,month,day)

    qs=fetch_1days_questions(tags,day0)
    filepath=save_raw_questions(qs,tags,day0)
    upload_to_s3(filepath,tags,day0)


if __name__=='__main__':
    fetch_save_upload()