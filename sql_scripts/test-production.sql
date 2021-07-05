-- ALL_COMPANY_DETAILS
SELECT 'Query Test 1: ALL_COMPANY_DETAILS' AS '';

SELECT *
FROM COMPANY_DETAILS
ORDER BY company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC
LIMIT 10;


-- COMPANY_DETAILS_FOR_CID
SELECT 'Query Test 2: COMPANY_DETAILS_FOR_CID' AS '';

SELECT *
FROM COMPANY_DETAILS
WHERE cid = 920417428
LIMIT 10;


-- ALL_JOB_DETAILS_FOR_CID
SELECT 'Query Test 3: ALL_JOB_DETAILS_FOR_CID' AS '';

SELECT *
FROM JOB_DETAILS
WHERE cid = 920417428
ORDER BY job_rating_rank ASC, job_salary_rank ASC
LIMIT 10;


-- HIRES_BY_TERM_FOR_CID
SELECT 'Query Test 4: HIRES_BY_TERM_FOR_CID' AS '';

SELECT
    term_num,
    COUNT(term_num) as hires
FROM PLACEMENT
WHERE cid = 920417428
GROUP BY term_num
ORDER BY term_num
LIMIT 10;


-- HIRES_BY_TERM_FOR_JID
SELECT 'Query Test 5: HIRES_BY_TERM_FOR_JID' AS '';

SELECT
    term_num,
    COUNT(term_num) as hires
FROM PLACEMENT
WHERE jid = 024154801
GROUP BY term_num
ORDER BY term_num
LIMIT 10;


-- ALL_JOB_DETAILS
SELECT 'Query Test 6: ALL_JOB_DETAILS' AS '';

SELECT *
FROM JOB_DETAILS
ORDER BY job_rating_rank ASC, job_salary_rank ASC, company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC
LIMIT 10;


-- JOB_DETAILS_FOR_JID
SELECT 'Query Test 7: JOB_DETAILS_FOR_JID' AS '';

SELECT *
FROM JOB_DETAILS
WHERE jid = 024154801
LIMIT 10;


-- ----------------------------------------------------------------------------
-- PRODUCTION TESTS FOR TAG AND REVIEW QUERIES - NOT IMPLEMENTED YET
-- ----------------------------------------------------------------------------

-- ALL_JOB_DETAILS_FOR_TAG
-- SELECT *
-- FROM JOB_TAG
-- NATURAL JOIN TAG
-- NATURAL JOIN JOB_DETAILS
-- WHERE TAG.label = %s
-- ORDER BY job_rating_rank ASC, job_salary_rank ASC, company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC;


-- ALL_TAGS
-- SELECT tid, label
-- FROM TAG;


-- ALL_TAGS_FOR_JID
-- SELECT *
-- FROM JOB_TAG
-- NATURAL JOIN TAG
-- NATURAL JOIN JOB
-- WHERE jid = 024154801;


-- ALL_REVIEWS_FOR_JID
-- SELECT *
-- FROM REVIEW
-- WHERE jid = 024154801;


-- INSERT_REVIEW_FOR_JID
-- INSERT INTO REVIEW(cid, jid, headline, review_body, rating)
-- SELECT
--     cid,
--     jid,
--     'headline' AS headline,
--     'review_body' AS review_body,
--     3 AS rating
-- FROM JOB
-- WHERE jid = 024154801;


-- REVIEW_FOR_RID
-- SELECT *
-- FROM REVIEW
-- WHERE rid = %s;
