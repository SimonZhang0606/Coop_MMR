ALL_COMPANY_DETAILS = """
SELECT
    COMPANY.cid,
    COMPANY.name,
    avg_salary,
    avg_rating
FROM COMPANY
LEFT OUTER JOIN (
    SELECT cid, AVG(salary) as avg_salary
    FROM PLACEMENT
    WHERE salary IS NOT NULL
    GROUP BY cid
) AS COMPANY_SALARY
ON COMPANY.cid = COMPANY_SALARY.cid
LEFT OUTER JOIN(
    SELECT cid, AVG(rating) as avg_rating
    FROM REVIEW
    WHERE rating IS NOT NULL
    GROUP BY cid
) AS COMPANY_REVIEW
ON COMPANY.cid = COMPANY_REVIEW.cid;
"""

COMPANY_DETAILS_FOR_CID = """
SELECT
    COMPANY.cid,
    COMPANY.name,
    avg_salary,
    avg_rating
FROM COMPANY
LEFT OUTER JOIN (
    SELECT cid, AVG(salary) as avg_salary
    FROM PLACEMENT
    WHERE salary IS NOT NULL
    GROUP BY cid
) AS COMPANY_SALARY
ON COMPANY.cid = COMPANY_SALARY.cid
LEFT OUTER JOIN(
    SELECT cid, AVG(rating) as avg_rating
    FROM REVIEW
    WHERE rating IS NOT NULL
    GROUP BY cid
) AS COMPANY_REVIEW
ON COMPANY.cid = COMPANY_REVIEW.cid
WHERE COMPANY.cid = %s;
"""

ALL_JOB_DETAILS_FOR_CID = """
SELECT
    JOB.cid,
    JOB.jid,
    COMPANY.name as company_name,
    JOB.title as job_title,
    avg_salary,
    avg_rating
FROM JOB
JOIN COMPANY ON JOB.cid = COMPANY.cid
LEFT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    WHERE salary IS NOT NULL
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN (SELECT jid, AVG(rating) as avg_rating
                    FROM REVIEW
                    WHERE rating IS NOT NULL
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid
WHERE COMPANY.cid = %s;
"""

HIRES_BY_TERM_FOR_CID = """
SELECT term_num, COUNT(term_num) as hires
FROM PLACEMENT
WHERE cid = %s
GROUP BY term_num;
"""

ALL_JOB_DETAILS = """
SELECT
    JOB.cid,
    JOB.jid,
    COMPANY.name as company_name,
    JOB.title as job_title,
    avg_salary,
    avg_rating
FROM JOB
JOIN COMPANY
ON JOB.cid = COMPANY.cid
LEFT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    WHERE salary IS NOT NULL
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN (SELECT jid, AVG(rating) as avg_rating
                    FROM REVIEW
                    WHERE rating IS NOT NULL
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid;
"""

JOB_DETAILS_FOR_JID = """
SELECT
    JOB.cid,
    JOB.jid,
    COMPANY.name as company_name,
    JOB.title as job_title,
    avg_salary,
    avg_rating
FROM JOB
JOIN COMPANY
ON JOB.cid = COMPANY.cid
LEFT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    WHERE salary IS NOT NULL
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN (SELECT jid, AVG(rating) as avg_rating
                    FROM REVIEW
                    WHERE rating IS NOT NULL
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid
WHERE JOB.jid = %s;
"""

ALL_JOB_DETAILS_FOR_TAG = """
SELECT
    JOB.cid,
    JOB.jid,
    COMPANY.name as company_name,
    JOB.title as job_title,
    avg_salary,
    avg_rating
FROM JOB_TAG
INNER JOIN TAG
ON JOB_TAG.tid = TAG.tid
INNER JOIN JOB
ON JOB_TAG.jid = JOB.jid
LEFT OUTER JOIN COMPANY
ON JOB.cid = COMPANY.cid
LEFT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    WHERE salary IS NOT NULL
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN (SELECT jid, AVG(rating) as avg_rating
                    FROM REVIEW
                    WHERE rating IS NOT NULL
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid
WHERE TAG.label = %s;
"""

ALL_TAGS = """
SELECT tid, label
FROM TAG
"""
