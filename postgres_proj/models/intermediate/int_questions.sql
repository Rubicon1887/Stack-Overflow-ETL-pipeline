SELECT 
    question_id,
    programming_language,
    tags,
    owner_id,
    owner_reputation,
    owner_name,
    is_answered,
    view_count,
    closed_unix_timestamp,
    answer_count,
    score,
    creation_unix_timestamp,
    question_date,
    upload_timestamp
FROM {{source('stackoverflow','questions')}}