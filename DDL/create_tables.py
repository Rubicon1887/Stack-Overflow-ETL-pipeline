import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

def create_questions_table():

    # public.questions definition
    sql="""
    CREATE TABLE public.questions (
        question_id bigint NOT NULL,
        programming_language varchar NULL,
        tags _varchar NULL,
        owner_id bigint NULL,
        owner_reputation bigint NULL,
        owner_name varchar NULL,
        is_answered boolean NULL,
        view_count bigint NULL,
        closed_date bigint NULL,
        answer_count bigint NULL,
        score bigint NULL,
        question_date date NULL,
        CONSTRAINT questions_pk PRIMARY KEY (question_id, programming_language)
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


if __name__=='__main__':
    create_questions_table()


# TODO: Load data into the table
# TODO: The table should be a "question-level" table. It needs to have a date as well
# TODO: question_id is a primary key. If a questions appears in both python and java questions, it'll appear twice. Something else needs to be a primary key. or do I just not make it a primary key?