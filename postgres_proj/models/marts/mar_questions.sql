{{ config(schema='marts') }}

WITH year_counts AS (
    SELECT programming_language,question_year,COUNT(DISTINCT question_id) AS question_count
    FROM {{ ref('int_questions') }}
    WHERE question_year!=2026
    GROUP BY programming_language,question_year
)

SELECT
    *,
    SUM(question_count) OVER(PARTITION BY question_year) AS year_total,
    ROUND(question_count/SUM(question_count) OVER(PARTITION BY question_year)*100,2) AS pct_share
FROM year_counts

-- TODO: Instead of raw counts per year, it's better to show the share of questions of each language (a %)