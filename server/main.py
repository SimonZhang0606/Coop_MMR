import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ThankMrGoose',
    database='coop_mmr',
)

cursor = connection.cursor()

# Example: print all table names


Command = """
SELECT COMPANY.name as company_name, JOB.title as job_title,
IFNULL(avg_salary, "missing") as avg_salary, IFNULL(avg_rating, "missing") as avg_rating
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

cursor.execute(Command)

json_output = json.dumps(cursor.fetchall())

connection.close()
