{{ config(schema='intermediate') }}

WITH questions AS (
    SELECT 
        question_id,
        programming_language,
        tags,
        owner_id,
        owner_reputation,
        owner_name,
        is_answered,
        view_count,
        to_timestamp(closed_unix_timestamp) AS closed_timestamp,
        (closed_unix_timestamp IS NOT NULL) AS is_closed,
        answer_count,
        score,
        TO_TIMESTAMP(creation_unix_timestamp) AS creation_timestamp,
        TO_TIMESTAMP(creation_unix_timestamp)::DATE AS question_date,
        upload_timestamp
    FROM {{ ref('stg_questions') }}
)

SELECT
    *,
    extract(year FROM creation_timestamp) AS question_year,
    extract(month FROM creation_timestamp) AS question_month,
    extract(day FROM creation_timestamp) AS question_day,
    extract(dow FROM creation_timestamp) AS question_dow
FROM questions

-- TODO: may add days_to_close