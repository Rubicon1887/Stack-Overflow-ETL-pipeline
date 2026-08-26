{{ config(schema='staging')}}

SELECT 
    question_id,
    "language" as programming_language,
    tags,
    user_id as owner_id,
    reputation as owner_reputation,
    display_name as owner_name,
    is_answered,
    view_count,
    closed_date as closed_unix_timestamp,
    answer_count,
    score,
    creation_date as creation_unix_timestamp,
    "current" as question_date,
    utc_timestamp_now as upload_timestamp
FROM {{ source('stackoverflow','questions') }}