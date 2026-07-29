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

class Extract:

    def __init__(self,day0,tag,backfill=False):

        self.day0=day0
        self.tag=tag
        self.backfill=backfill
    
    def fetch_1days_questions(self):

        day1=self.day0+timedelta(days=1)

        fromdate=int(datetime.combine(self.day0,time.min,tzinfo=timezone.utc).timestamp())
        todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

        if not self.backfill: print(colored(f'1 - Fetching Stack Overflow questions from {self.day0} tagged with {self.tag}','yellow'))
        qs=SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=self.tag)
        if not self.backfill: print(colored(f'2 - Successfully fetched {len(qs['items'])} questions','green'))

        return qs

    def save_raw_questions(self,qs):

        path=Path(
            r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
            f'{self.day0.year}',
            f'{self.day0.month:02d}',
            f'{self.day0.day:02d}'
        )

        path.mkdir(parents=True,exist_ok=True)
        filepath=path/f'{self.tag}_questions.json'

        with open(filepath,'w',encoding='utf-8') as f:
            json.dump(qs,f,indent=2)
        if not self.backfill: print(colored(f'3 - Saved {self.day0} data to {filepath}','blue'))

        return filepath

    def upload_to_s3(self,filepath):

        key=(
            f'raw/'
            f'{self.day0.year}/'
            f'{self.day0.month:02d}/'
            f'{self.day0.day:02d}/'
            f'{self.tag}_questions.json'
        )

        client.upload_file(filepath,bucket_name,key)
        if not self.backfill: print(colored(f'4 - Uploaded {self.day0} file to s3://{bucket_name}/{key}','magenta')) # may wanna print tag somewhere