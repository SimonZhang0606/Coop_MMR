AGGREGATE_COMPANIES = """
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

JOBS_BY_COMPANY = """
SELECT JOB.jid, title, avg_salary, avg_review
FROM JOB
LEFT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    WHERE salary IS NOT NULL
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
LEFT OUTER JOIN (SELECT jid, AVG(rating) as avg_review
                    FROM REVIEW
                    WHERE rating IS NOT NULL
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid
WHERE cid = %s;
"""

STUDENTS_HIRED_BY_TERM = """
SELECT term_num, COUNT(term_num) as hires
FROM PLACEMENT
WHERE cid = %s
GROUP BY term_num;
"""

AGGREGATE_JOBS = """
SELECT
    JOB.jid,
    COMPANY.name as company_name,
    JOB.title as job_title,
    avg_salary,
    avg_rating
FROM JOB
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
ORDER BY JOB_SALARY.avg_salary DESC;
"""

JOBS_BY_TAG = """
SELECT JOB.jid, JOB.title
FROM JOB_TAG
JOIN TAG
ON JOB_TAG.tid = TAG.tid
JOIN JOB
ON JOB.jid = JOB_TAG.jid
WHERE TAG.label = %s;
"""
