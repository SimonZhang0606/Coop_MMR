import flask
import json
import argparse
import mysql.connector


def list_jobs(connection):
    cursor = connection.cursor()

    cursor.execute("""
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
    """)

    return cursor.fetchall()


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

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/jobs', methods=['GET'])
    def home():
        return json.dumps(list_jobs(connection))

    app.run()

    connection.close()
