with questions as (
    SELECT 
        question_id,
        programming_language,
        tags,
        owner_id,
        owner_reputation,
        owner_name,
        is_answered,
        view_count,
        to_timestamp(closed_unix_timestamp) as closed_timestamp,
        answer_count,
        score,
        to_timestamp(creation_unix_timestamp) as creation_timestamp,
        to_timestamp(creation_unix_timestamp)::date as question_date,
        upload_timestamp
    FROM {{ref('stg_questions')}}
)

SELECT
    *,
    extract(year from creation_timestamp) as question_year,
    extract(month from creation_timestamp) as question_month,
    extract(day from creation_timestamp) as question_day,
    extract(dow from creation_timestamp) as question_dow
FROM questions