ALL_COMPANY_DETAILS = """
SELECT *
FROM COMPANY_DETAILS
"""

COMPANY_DETAILS_FOR_CID = """
SELECT *
FROM COMPANY_DETAILS
WHERE cid = %s;
"""

ALL_JOB_DETAILS_FOR_CID = """
SELECT *
FROM JOB_DETAILS
WHERE cid = %s;
"""

HIRES_BY_TERM_FOR_CID = """
SELECT term_num, COUNT(term_num) as hires
FROM PLACEMENT
WHERE cid = %s
GROUP BY term_num;
"""

ALL_JOB_DETAILS = """
SELECT *
FROM JOB_DETAILS;
"""

JOB_DETAILS_FOR_JID = """
SELECT *
FROM JOB_DETAILS
WHERE jid = %s;
"""

ALL_JOB_DETAILS_FOR_TAG = """
SELECT
    JOB_DETAILS.cid,
    company_name,
    JOB_DETAILS.jid,
    job_mmr,
    job_title,
    company_min_salary,
    company_avg_salary,
    company_max_salary,
    company_avg_rating,
    job_min_salary,
    job_avg_salary,
    job_max_salary,
    job_avg_rating
FROM JOB_TAG
JOIN TAG
ON JOB_TAG.tid = TAG.tid
JOIN JOB_DETAILS
ON JOB_TAG.jid = JOB_DETAILS.jid
WHERE TAG.label = %s;
"""

ALL_TAGS = """
SELECT tid, label
FROM TAG
"""
