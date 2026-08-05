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

    def __init__(self):

        self.SITE=StackAPI('stackoverflow',key=api_key)
        self.SITE.page_size=100
        self.SITE.max_pages=15

        self.client=boto3.client('s3')
    
    def fetch_1days_questions(self,day0,tag):

        day1=day0+timedelta(days=1)

        fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
        todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

        qs=self.SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=tag)

        return qs

    # save json LOCALLY
    def save_raw_questions(self,day0,tag,qs):

        path=Path(
            r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
            f'{day0.year}',
            f'{day0.month:02d}',
            f'{day0.day:02d}'
        )

        path.mkdir(parents=True,exist_ok=True)
        filepath=path/f'{tag}_questions.json'

        with open(filepath,'w',encoding='utf-8') as f:
            json.dump(qs,f,indent=2)

        return filepath

    # upload LOCAL json to S3
    def upload_to_S3(self,day0,tag,file):

        key=(
            f'raw/'
            f'{day0.year}/'
            f'{day0.month:02d}/'
            f'{day0.day:02d}/'
            f'{tag}_questions.json'
        )

        if type(file)is bytes:
            self.client.put_object(Body=file,Bucket=bucket_name,Key=key)
        else:
            self.client.upload_file(Filename=file,Bucket=bucket_name,Key=key)

        return bucket_name,key

# dictionary for tags

# TODO: change/add a method (put_object) to upload jsons directly to S3 after fetching. Idea - skip save_raw_questions(), alter upload_to_S3()'s behavior based on whether it receives a filepath or dict with questions