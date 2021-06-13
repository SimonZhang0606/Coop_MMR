SELECT '----------------------' AS '';
SELECT 'BROWSE ALL COMPANY PAGE' AS '';
SELECT '----------------------' AS '';
-- View company salary average
SELECT COMPANY.cid, COMPANY.name, COMPANY_SALARY.avg_salary
FROM COMPANY 
LEFT OUTER JOIN (
    SELECT cid, AVG(salary) as avg_salary
    FROM PLACEMENT
    WHERE salary IS NOT NULL
    GROUP BY cid
) AS COMPANY_SALARY
ON COMPANY.cid = COMPANY_SALARY.cid
ORDER BY COMPANY_SALARY.avg_salary DESC;

-- View company review average
SELECT COMPANY.cid, COMPANY.name, COMPANY_REVIEW.avg_review
FROM COMPANY
LEFT OUTER JOIN(
    SELECT cid, AVG(rating) as avg_review
    FROM REVIEW 
    WHERE rating IS NOT NULL
    GROUP BY cid
) AS COMPANY_REVIEW
ON COMPANY.cid = COMPANY_REVIEW.cid 
ORDER BY COMPANY_REVIEW.avg_review DESC;


SELECT '----------------------' AS '';
SELECT 'COMPANY PAGE FOR EACH COMPANY' AS '';
SELECT '----------------------' AS '';

-- VIEW NUMBER OF JOBS POSTED BY COMPANY
SELECT count(*) 
FROM JOB
WHERE JOB.cid = 567586557;

SELECT '----------------------' AS '';
-- VIEW NUMBER OF PLACEMENTS POSTED BY COMPANY 
SELECT count(*) 
FROM PLACEMENT
WHERE PLACEMENT.cid = 567586557;

SELECT '----------------------' AS '';
-- VIEW AVERAGE RATING OF THE COMPANY
SELECT cid, avg(rating)
from REVIEW 
WHERE cid = 567586557
GROUP BY cid;

SELECT '----------------------' AS '';
-- VIEW AVERAGE SALARY OF THE COMPANY
SELECT cid, avg(salary)
from PLACEMENT
WHERE cid = 567586557
GROUP BY cid;

SELECT '----------------------' AS '';
-- VIEW TERMS HIRED BY COMPANY 
SELECT term_num, COUNT(term_num)
FROM (SELECT * 
        FROM PLACEMENT
        WHERE cid = 567586557
    ) as PLACES
GROUP BY term_num;

SELECT '----------------------' AS '';
SELECT 'LIST ALL JOBS POSTED BY THE COMPANY AND THEIR RELATED INFO' AS '';
SELECT 'INCLUDING average salary and rating' AS '';
SELECT '----------------------' AS '';

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
WHERE cid = 567586557;

-- Note that the rating calculation is a little bit more complicated 
-- than a simple SQL query so for space purposes we will not be including 
-- it here. In general however, we will be treating each latter coop job 
-- as winning the "battle" against a earlier coop job, and awarding mmr to 
-- the latter job. See the link below for a more detailed description