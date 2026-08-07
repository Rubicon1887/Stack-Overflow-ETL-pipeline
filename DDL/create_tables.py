import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

# public.questions definition
sql="""
CREATE TABLE public.questions (
	question_id bigint NOT NULL,
	tags _varchar NULL,
	owner_reputation bigint NULL,
	owner_name varchar NULL,
	is_answered boolean NULL,
	view_count bigint NULL,
	answer_count bigint NULL,
	score bigint NULL,
	CONSTRAINT questions_pk PRIMARY KEY (question_id)
);
"""

cnxn_params={
    'host':os.getenv('DB_HOST'),
    'dbname':os.getenv('POSTGRES_DB'),
    'user':os.getenv('POSTGRES_USER'),
    'password':os.getenv('POSTGRES_PASSWORD')
}

with psycopg.connect(**cnxn_params) as cnxn:
    with cnxn.cursor() as cur:
        cur.execute(sql)


# TODO: Load data into the table
# TODO: organize into a method/s
