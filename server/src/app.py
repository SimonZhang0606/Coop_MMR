import json
from os import environ
from pprint import pprint
from flask import Flask
from flask_cors import CORS
import mysql.connector


def list_jobs(connection):
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        JOB.jid as jid,
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
    """)

    for job in cursor.fetchall():
        jid, company_name, job_title, avg_salary, avg_rating = job
        job_dict = {
            'jid': int(jid),
            'company_name': str(company_name),
            'job_title': str(job_title),
        }
        if avg_salary is not None:
            job_dict['avg_salary'] = float(avg_salary)
        if avg_rating is not None:
            job_dict['avg_rating'] = float(avg_rating)
        yield job_dict


host = environ.get('DB_HOST')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')
database = environ.get('DB_DATABASE')

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True


@app.route('/jobs', methods=['GET'])
def home():
    jobs_list = list(list_jobs(connection))
    return json.dumps(jobs_list)


if __name__ == '__main__':
    app.run()
    connection.close()
