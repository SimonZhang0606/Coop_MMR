
------------
-- BROWSE ALL COMPANY PAGE
------------

-- View company salary average
SELECT COMPANY_SALARY.cid, COMPANY.name, COMPANY_SALARY.avg_salary
FROM COMPANY 
LEFT OUTER JOIN (
    SELECT cid, AVG(salary) as avg_salary
    FROM PLACEMENT
    GROUP BY cid
) AS COMPANY_SALARY
ON COMPANY.cid = COMPANY_SALARY.cid
ORDER BY COMPANY_SALARY.avg_salary DESC 

-- View company review average
SELECT COMPANY_REVIEW.cid, COMPANY.name, COMPANY_REVIEW.avg_review
FROM COMPANY
LEFT OUTER JOIN(
    SELECT cid, AVG(rating) as avg_review
    FROM REVIEW 
    GROUP BY cid
) AS COMPANY_REVIEW
ON COMPANY.cid = COMPANY_REVIEW.cid 
ORDER BY COMPANY_REVIEW.avg_review DESC 

------------
-- COMPANY PAGE FOR EACH COMPANY
------------

-- VIEW NUMBER OF JOBS POSTED BY COMPANY
SELECT count(*) 
FROM JOB
WHERE JOB.cid = search_input

-- VIEW NUMBER OF PLACEMENTS POSTED BY COMPANY 
SELECT count(*) 
FROM PLACEMENT
WHERE PLACEMENT.cid = search_input

-- VIEW AVERAGE RATING OF THE COMPANY
SELECT avg(rating)
from REVIEW 
GROUP BY cid
WHERE cid = search_input

-- VIEW AVERAGE SALARY OF THE COMPANY
SELECT avg(salary)
from PLACEMENT
GROUP BY cid
WHERE cid = search_input

-- VIEW TERMS HIRED BY COMPANY 
SELECT term_num, COUNT(term_num)
FROM (SELECT * 
        FROM PLACEMENT
        WHERE cid = search_input
    )
GROUP BY term_num

-- LIST ALL JOBS POSTED BY THE COMPANY AND THEIR RELATED INFO
-- INCLUDING average salary and rating
SELECT avg_salary, avg_review
FROM JOB
RIGHT OUTER JOIN (SELECT jid, AVG(salary) as avg_salary
                    FROM PLACEMENT
                    GROUP BY jid
                ) as JOB_SALARY
ON JOB.jid = JOB_SALARY.jid
RIGHT OUTER JOIN (SELECT jid, AVG(rating) as avg_review
                    FROM REVIEW
                    GROUP BY jid
                ) as JOB_RATING
ON JOB.jid = JOB_RATING.jid
WHERE cid = search_input

-- Note that the rating calculation is a little bit more complicated 
-- than a simple SQL query so for space purposes we will not be including 
-- it here. In general however, we will be treating each latter coop job 
-- as winning the "battle" against a earlier coop job, and awarding mmr to 
-- the latter job. See the link below for a more detailed description