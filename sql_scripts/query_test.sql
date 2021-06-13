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