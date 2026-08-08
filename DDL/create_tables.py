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