ALL_COMPANY_DETAILS = """
SELECT *
FROM COMPANY_DETAILS
ORDER BY company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC;
"""

COMPANY_DETAILS_FOR_CID = """
SELECT *
FROM COMPANY_DETAILS
WHERE cid = %s;
"""

ALL_JOB_DETAILS_FOR_CID = """
SELECT *
FROM JOB_DETAILS
WHERE cid = %s
ORDER BY job_rating_rank ASC, job_salary_rank ASC;
"""

HIRES_BY_TERM_FOR_CID = """
SELECT
    term_num,
    COUNT(term_num) as hires
FROM PLACEMENT
WHERE cid = %s
GROUP BY term_num
ORDER BY term_num;
"""

HIRES_BY_TERM_FOR_JID = """
SELECT
    term_num,
    COUNT(term_num) as hires
FROM PLACEMENT
WHERE jid = %s
GROUP BY term_num
ORDER BY term_num;
"""

ALL_JOB_DETAILS = """
SELECT *
FROM JOB_DETAILS
ORDER BY job_rating_rank ASC, job_salary_rank ASC, company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC;
"""

JOB_DETAILS_FOR_JID = """
SELECT *
FROM JOB_DETAILS
WHERE jid = %s;
"""

ALL_JOB_DETAILS_FOR_TAG = """
SELECT *
FROM JOB_TAG
NATURAL JOIN TAG
NATURAL JOIN JOB_DETAILS
WHERE TAG.label = %s
ORDER BY job_rating_rank ASC, job_salary_rank ASC, company_mmr_rank ASC, company_rating_rank ASC, company_salary_rank ASC;
"""

ALL_TAGS = """
SELECT tid, label
FROM TAG;
"""

ALL_TAGS_FOR_JID = """
SELECT *
FROM JOB_TAG
NATURAL JOIN TAG
NATURAL JOIN JOB
WHERE jid = %s;
"""

ALL_REVIEWS_FOR_JID = """
SELECT *
FROM REVIEW
WHERE jid = %s;
"""

INSERT_REVIEW_FOR_JID = """
INSERT INTO REVIEW(cid, jid, headline, review_body, rating)
SELECT
    cid,
    jid,
    %s AS headline,
    %s AS review_body,
    %s AS rating
FROM JOB
WHERE jid = %s;
"""

REVIEW_FOR_RID = """
SELECT *
FROM REVIEW
WHERE rid = %s;
"""
