from stackapi import StackAPI
from datetime import datetime,time,timedelta,timezone
from termcolor import colored
from dotenv import load_dotenv
import os

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