import psycopg
from dotenv import load_dotenv
import os
from termcolor import colored

load_dotenv()

cnxn_params={
    'host':os.getenv('DB_HOST'),
    'dbname':os.getenv('POSTGRES_DB'),
    'user':os.getenv('POSTGRES_USER'),
    'password':os.getenv('POSTGRES_PASSWORD')
}

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
        upload_timestamp timestamp with time zone NULL,
        CONSTRAINT questions_pk PRIMARY KEY (question_id, programming_language)
    );
    """

    with psycopg.connect(**cnxn_params) as cnxn:
        with cnxn.cursor() as cur:
            cur.execute(sql)

    print(colored('CREATED TABLE public.questions','blue'))


def delete_questions_table():

    sql="""
    DROP TABLE IF EXISTS public.questions
    """

    with psycopg.connect(**cnxn_params) as cnxn:
            with cnxn.cursor() as cur:
                cur.execute(sql)

    print(colored('DELETED TABLE public.questions','blue'))


def truncate_questions_table():

    sql="""
    TRUNCATE TABLE public.questions
    """

    with psycopg.connect(**cnxn_params) as cnxn:
            with cnxn.cursor() as cur:
                cur.execute(sql)

    print(colored('PURGED TABLE public.questions','blue'))


if __name__=='__main__':

    delete_questions_table()
    create_questions_table()
    # truncate_questions_table()


# TODO: convert closed_date to actual date
# TODO: also keep the creation_date (which is actually a timestamp)
# TODO: question_day_of_week
# TODO: closed_date -> null/not null is_closed