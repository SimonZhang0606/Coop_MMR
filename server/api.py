import argparse
import json
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--user', type=str, default='root')
    parser.add_argument('--password', type=str, default='ThankMrGoose')
    parser.add_argument('--database', type=str, default='coop_mmr')
    args = parser.parse_args()

    print(args)
    connection = mysql.connector.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database,
    )

    app = Flask(__name__)
    CORS(app)

    app.config['DEBUG'] = True

    @app.route('/jobs', methods=['GET'])
    def home():
        jobs_list = list(list_jobs(connection))
        pprint(jobs_list)
        return json.dumps(jobs_list)

    app.run()

    connection.close()
