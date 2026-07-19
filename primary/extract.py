from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone
from termcolor import colored
from dotenv import load_dotenv
import os
from pathlib import Path
import json

load_dotenv()

apikey=os.getenv('STACK_API_KEY')

def fetch_yesterdays_questions(tags): # I might not need start_date and end_date
    
    SITE=StackAPI('stackoverflow',key=apikey)
    SITE.page_size=100
    SITE.max_pages=15

    today=datetime.now(timezone.utc).date()
    yesterday=today-timedelta(days=1)

    fromdate=int(datetime.combine(yesterday,time.min,tzinfo=timezone.utc).timestamp())
    todate=int(datetime.combine(today,time.min,tzinfo=timezone.utc).timestamp())

    print(colored(f'Fetching Stack Overflow questions from {yesterday} tagged with {tags}','yellow'))
    qs=SITE.fetch('questions',fromdate=fromdate,todate=todate,tagged=tags)
    print(colored(f'Successfully fetched {len(qs['items'])} questions','green'))

    return qs

def save_raw_questions(tags):
    
    data=fetch_yesterdays_questions(tags)

    now=datetime.now()
    path=Path(
        r'C:\Users\athar\Documents\GitHub\personal project\Stack Overflow ETL pipeline\S3 data',
        f'{now.year}',
        f'{now.month:02d}',
        f'{now.day:02d}'
    )

    path.mkdir(parents=True,exist_ok=True)
    filepath=path/f'{tags}_questions.json'

    with open(filepath,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)
    print(f'Saved {now.date()} data to {filepath}')

if __name__=='__main__':
    save_raw_questions('python')