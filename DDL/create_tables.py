import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

host=os.getenv('DB_HOST')
print(host)

# cnxn=psycopg.connect(
#     host='localhost',
#     dbname='stkof',
#     user='postgres',
#     password='postgres'
# )

# # public.questions definition
# sql="""
# CREATE TABLE public.questions (
# 	question_id bigint NOT NULL,
# 	tags _varchar NULL,
# 	owner_reputation bigint NULL,
# 	owner_name varchar NULL,
# 	is_answered boolean NULL,
# 	view_count bigint NULL,
# 	answer_count bigint NULL,
# 	score bigint NULL,
# 	CONSTRAINT questions_pk PRIMARY KEY (question_id)
# );
# """

# TODO: Cree a SQL file to create postgres tables