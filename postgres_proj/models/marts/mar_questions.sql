{{ config(schema='marts') }}

SELECT programming_language,question_year,COUNT(DISTINCT question_id)
FROM {{ ref('int_questions') }}
WHERE question_year!=2026
GROUP BY programming_language,question_year
ORDER BY programming_language,question_year ASC

-- TODO: Instead of raw counts per year, it's better to show the share of questions of each language (a %)