import json

from flask import Flask, request
from flask_cors import CORS
import mysql.connector

from utils.mysql import connect_db, get_cursor
from utils.serialization import serialize
from queries import *


def aggregate_companies(cursor):
    cursor.execute(AGGREGATE_COMPANIES)
    for company in cursor:
        print(company)
        yield {
            'cid': serialize(company.cid, as_type=int),
            'name': company.name,
            'avg_salary': serialize(company.avg_salary, as_type=float, nullable=True),
            'avg_rating': serialize(company.avg_rating, as_type=float, nullable=True),
        }


def jobs_by_company(cursor, cid):
    cursor.execute(JOBS_BY_COMPANY, (cid,))
    for job in cursor:
        print(job)
        yield {
            'jid': serialize(job.jid, as_type=int),
            'title': job.title,
            'avg_salary': serialize(job.avg_salary, as_type=float, nullable=True),
            'avg_review': serialize(job.avg_review, as_type=float, nullable=True),
        }


def students_hired_by_term(cursor, cid):
    cursor.execute(STUDENTS_HIRED_BY_TERM, (cid,))
    for term in cursor:
        print(term)
        yield {
            'term_num': serialize(term.term_num, as_type=int),
            'hires': serialize(term.hires, as_type=int),
        }


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

connection = connect_db()


@app.route('/companies', methods=['GET'])
def companies():
    with get_cursor(connection) as cursor:
        res = list(aggregate_companies(cursor))
        return json.dumps(res)


@app.route('/companies/<cid>', methods=['GET'])
def company(cid):
    with get_cursor(connection) as cursor:
        res = {
            'jobs': list(jobs_by_company(cursor, cid)),
            'hires_by_term': list(students_hired_by_term(cursor, cid)),
        }
        return json.dumps(res)


@app.route('/jobs', methods=['GET'])
def jobs():
    with get_cursor(connection) as cursor:
        if tag := request.args.get('tag', None):
            res = list(jobs_by_tag(cursor, tag))
        else:
            res = list(aggregate_jobs(cursor))
        return json.dumps(res)


if __name__ == '__main__':
    app.run()
    connection.close()
