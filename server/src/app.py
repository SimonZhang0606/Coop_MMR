import json

from flask import Flask
from flask_cors import CORS
import mysql.connector

from utils.mysql import open_connection, get_cursor
from utils.serialization import serialize
from queries import AGGREGATE_JOBS


def list_jobs(cursor):
    cursor.execute(AGGREGATE_JOBS)
    for job in cursor:
        yield {
            'jid': serialize(job.jid, as_type=int),
            'company_name': job.company_name,
            'job_title': job.job_title,
            'avg_salary': serialize(job.avg_salary, as_type=float, nullable=True),
            'avg_rating': serialize(job.avg_rating, as_type=float, nullable=True),
        }


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

connection = open_connection()


@app.route('/jobs', methods=['GET'])
def home():
    with get_cursor(connection) as cursor:
        jobs_list = list(list_jobs(cursor))
    return json.dumps(jobs_list)


if __name__ == '__main__':
    app.run()
    cnx.close()
