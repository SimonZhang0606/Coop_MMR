import json

from flask import Flask, request
from flask_cors import CORS
import mysql.connector

from utils.mysql import open_connection, get_cursor
from utils.serialization import serialize
from queries import *


def aggregate_jobs(cursor):
    cursor.execute(AGGREGATE_JOBS)
    for job in cursor:
        print(job)
        yield {
            'jid': serialize(job.jid, as_type=int),
            'company_name': job.company_name,
            'job_title': job.job_title,
            'avg_salary': serialize(job.avg_salary, as_type=float, nullable=True),
            'avg_rating': serialize(job.avg_rating, as_type=float, nullable=True),
        }


def jobs_by_tag(cursor, tag):
    print(tag)
    cursor.execute(JOBS_BY_TAG, (tag,))
    for job in cursor:
        print(job)
        yield {
            'jid': serialize(job.jid, as_type=int),
            'title': job.title,
        }


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

connection = open_connection()


@app.route('/jobs', methods=['GET'])
def jobs():
    with get_cursor(connection) as cursor:
        if tag := request.args.get('tag', None):
            jobs = list(jobs_by_tag(cursor, tag))
        else:
            jobs = list(aggregate_jobs(cursor))
        return json.dumps(jobs)


if __name__ == '__main__':
    app.run()
    connection.close()
