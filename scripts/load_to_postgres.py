import boto3
from datetime import date,timedelta,datetime,timezone
from dotenv import load_dotenv
import os
import json
import psycopg

load_dotenv()

client=boto3.client('s3')
languages=['python','java','javascript','typescript','c#']
cnxn_params={
    'host':os.getenv('DB_HOST'),
    'dbname':os.getenv('POSTGRES_DB'),
    'user':os.getenv('POSTGRES_USER'),
    'password':os.getenv('POSTGRES_PASSWORD')
}

def load_to_db():

    utc_timestamp_now=datetime.now(timezone.utc)

    start_date=date(2011,1,1)
    end_date=date(2026,7,31) # for now, let the backfill end on 2026,7,31

    current=start_date

    with psycopg.connect(**cnxn_params) as cnxn:
        with cnxn.cursor() as cur:
            with cur.copy('COPY public.questions (question_id,language,tags,user_id,reputation,display_name,is_answered,view_count,closed_date,answer_count,score,'
                          'creation_date,current,utc_timestamp_now) FROM STDIN') as copy:

                while current<=end_date:
                    for language in languages:

                        key=(
                            f'raw/'
                            f'{current.year}/'
                            f'{current.month:02d}/'
                            f'{current.day:02d}/'
                            f'{language}_questions.json'
                        )

                        obj=client.get_object(Bucket=os.getenv('S3_BUCKET_NAME'),Key=key)
                        data=obj['Body'].read().decode('utf-8')
                        qs=json.loads(data)['items']

                        for q in qs:

                            question_id=q['question_id']
                            # language
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
                            # current
                            # utc_timestamp_now

                            copy.write_row((question_id,language,tags,user_id,reputation,display_name,is_answered,view_count,closed_date,answer_count,score,creation_date,current,utc_timestamp_now))

                    current+=timedelta(days=1)


if __name__=='__main__':
    load_to_db()
               

# TODO: since this loading action needs to be performed for both the backfill and new daily questions, shall I have it be in primary and call in scripts here? 
# db_backfill.py and db_daily.py

# TODO: compartmentalize the actions in load_to_db(), separate them out into a function to generate rows from S3, and another with the connection, cursor, copy, and date loop.
# This should be resuable for a backfill and a daily job

# However, the load_to_postgres script is separate from the the backfill script ON PURPOSE, because while the API has a quota, S3 doesn't, so this script isn't restricted to working
# on 2 years' data at a time, unlike backfill.py. So I only need to worry about integrating it in the daily.py script, NOT backfill.py.