import boto3
from datetime import date,timedelta
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

    start_date=date(2013,1,1)
    end_date=date(2013,12,31)

    current=start_date

    with psycopg.connect(**cnxn_params) as cnxn:
        with cnxn.cursor() as cur:
            with cur.copy('COPY public.questions (question_id,programming_language,tags,owner_id,owner_reputation,owner_name,is_answered,view_count,closed_date,answer_count,score,question_date) FROM STDIN') as copy:

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
                            programming_language=language
                            tags=q['tags']
                            owner_id=q['owner'].get('user_id')
                            owner_reputation=q['owner'].get('reputation')
                            owner_name=q['owner'].get('display_name')
                            is_answered=q['is_answered']
                            view_count=q['view_count']
                            closed_date=q.get('closed_date')
                            answer_count=q['answer_count']
                            score=q['score']
                            question_date=current

                            copy.write_row((question_id,programming_language,tags,owner_id,owner_reputation,owner_name,is_answered,view_count,closed_date,answer_count,score,question_date))

                    current+=timedelta(days=1)


if __name__=='__main__':
    load_to_db()
               

# TODO: Add upload date to table
# TODO: since this loading action needs to be performed for both the backfill and new daily questions, shall I have it be in primary and call in scripts here? db_backfill.py and db_daily.py