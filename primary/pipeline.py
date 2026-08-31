from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone,date
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import boto3
import psycopg

load_dotenv()

api_key=os.getenv('STACK_API_KEY')
bucket_name=os.getenv('S3_BUCKET_NAME')

cnxn_params={
    'host':os.getenv('DB_HOST'),
    'dbname':os.getenv('POSTGRES_DB'),
    'user':os.getenv('POSTGRES_USER'),
    'password':os.getenv('POSTGRES_PASSWORD')
}

class StackOverflowPipeline:

    def __init__(self):

        self.SITE=StackAPI('stackoverflow',key=api_key)
        self.SITE.page_size=100
        self.SITE.max_pages=15

        self.client=boto3.client('s3')

        self.utc_timestamp_now=datetime.now(timezone.utc)

    # Stack Overflow -> python variable qs (memory) through the API
    def fetch_1days_questions(self,day0,lang):

        day1=day0+timedelta(days=1)

        fromdate=int(datetime.combine(day0,time.min,tzinfo=timezone.utc).timestamp())
        todate=int(datetime.combine(day1,time.min,tzinfo=timezone.utc).timestamp())

        qs=self.SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=lang)

        return qs

    # save LOCALLY as json - unused
    def save_raw_questions(self,day0,lang,qs):

        path=Path(
            r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
            f'{day0.year}',
            f'{day0.month:02d}',
            f'{day0.day:02d}'
        )

        path.mkdir(parents=True,exist_ok=True)
        filepath=path/f'{lang}_questions.json'

        with open(filepath,'w',encoding='utf-8') as f:
            json.dump(qs,f,indent=2)

        return filepath

    # upload LOCAL jsons to S3/in-memory data to S3 as json
    def upload_to_S3(self,day0,lang,file):

        key=(
            f'raw/'
            f'{day0.year}/'
            f'{day0.month:02d}/'
            f'{day0.day:02d}/'
            f'{lang}_questions.json'
        )

        if type(file)is bytes:
            self.client.put_object(Body=file,Bucket=bucket_name,Key=key)
        else: # file is filepath and saved locally
            self.client.upload_file(Filename=file,Bucket=bucket_name,Key=key)

        return bucket_name,key

    def load_to_db(self,day0,lang,qs):

        with psycopg.connect(**cnxn_params) as cnxn:
            with cnxn.cursor() as cur:
                with cur.copy('COPY public.questions (question_id,language,tags,user_id,reputation,display_name,is_answered,view_count,closed_date,answer_count,score,'
                            'creation_date,current,utc_timestamp_now) FROM STDIN') as copy:     

                    for q in qs:
                        
                        question_id=q['question_id']
                        language=lang
                        tags=q['tags']
                        user_id=q['owner'].get('user_id')
                        reputation=q['owner'].get('reputation')
                        display_name=q['owner'].get('display_name')
                        is_answered=q['is_answered']
                        view_count=q['view_count']
                        closed_date=q.get('closed_date') # the json payload carries Unix timestamps (seconds since the Unix epoch)
                        answer_count=q['answer_count']
                        score=q['score']
                        creation_date=q['creation_date']
                        current=day0 # question date
                        utc_timestamp_now=self.utc_timestamp_now

                        copy.write_row((question_id,language,tags,user_id,reputation,display_name,is_answered,view_count,closed_date,answer_count,score,creation_date,current,utc_timestamp_now))                       


# dictionary for tags
# split postgres table by tags