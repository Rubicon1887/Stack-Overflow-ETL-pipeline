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

class Extract:

    def __init__(self,tag,backfill=False):

        self.tag=tag
        self.backfill=backfill

        self.SITE=StackAPI('stackoverflow',key=api_key)
        self.SITE.page_size=100
        self.SITE.max_pages=15

        self.client=boto3.client('s3')
    
    def fetch_1days_questions(self,day0):

        day1=day0+timedelta(days=1)

        fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
        todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

        if not self.backfill: print(colored(f'1 - Fetching Stack Overflow questions from {day0} tagged with {self.tag}','yellow'))
        qs=self.SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=self.tag)
        if not self.backfill: print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

        return qs

    # save json LOCALLY
    def save_raw_questions(self,day0,qs):

        path=Path(
            r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
            f'{day0.year}',
            f'{day0.month:02d}',
            f'{day0.day:02d}'
        )

        path.mkdir(parents=True,exist_ok=True)
        filepath=path/f'{self.tag}_questions.json'

        with open(filepath,'w',encoding='utf-8') as f:
            json.dump(qs,f,indent=2)
        if not self.backfill: print(colored(f'3 - Saved {day0} data to {filepath}','blue'))

        return filepath

    # upload LOCAL json to S3
    def upload_to_s3(self,day0,filepath):

        key=(
            f'raw/'
            f'{day0.year}/'
            f'{day0.month:02d}/'
            f'{day0.day:02d}/'
            f'{self.tag}_questions.json'
        )

        self.client.upload_file(filepath,bucket_name,key)
        if not self.backfill: print(colored(f'4 - Uploaded {day0} file to s3://{bucket_name}/{key}','magenta'))

# may wanna print tag somewhere
# add functionality to add questions with other tags
# try backfilling for a month, then maybe a year, account for multiple programming languages
# maybe add a method to check quota
# the print statements could be in daily.py/backfill.py