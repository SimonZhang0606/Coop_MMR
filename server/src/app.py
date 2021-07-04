import json

from flask import Flask, request
from flask_cors import CORS

from utils.db import DB
from utils.serialization import serialize_company_details, serialize_job_details, serialize_tag
from queries import *


def all_company_details(cursor):
    cursor.execute(ALL_COMPANY_DETAILS)
    for cd in cursor:
        print(cd)
        yield serialize_company_details(cd)


def company_details_for_cid(cursor, cid):
    print(cid)
    cursor.execute(COMPANY_DETAILS_FOR_CID, (cid,))
    cd = cursor.fetchone()
    print(cd)
    return serialize_company_details(cd)


def all_job_details_for_cid(cursor, cid):
    print(cid)
    cursor.execute(ALL_JOB_DETAILS_FOR_CID, (cid,))
    for jd in cursor:
        print(jd)
        yield serialize_job_details(jd)


def hires_by_term_for_cid(cursor, cid):
    print(cid)
    cursor.execute(HIRES_BY_TERM_FOR_CID, (cid,))
    for term in cursor:
        print(term)
        yield {
            'term_num': int(term.term_num),
            'hires': int(term.hires),
        }


def all_job_details(cursor):
    cursor.execute(ALL_JOB_DETAILS)
    for jd in cursor:
        print(jd)
        yield serialize_job_details(jd)


def job_details_for_jid(cursor, jid):
    print(jid)
    cursor.execute(JOB_DETAILS_FOR_JID, (jid,))
    jd = cursor.fetchone()
    print(jd)
    return serialize_job_details(jd)


def all_job_details_for_tag(cursor, tag):
    print(tag)
    cursor.execute(ALL_JOB_DETAILS_FOR_TAG, (tag,))
    for jd in cursor:
        print(jd)
        yield serialize_job_details(jd)


def all_tags(cursor):
    cursor.execute(ALL_TAGS)
    for tag in cursor:
        print(tag)
        yield serialize_tag(tag)


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True


@app.route('/companies', methods=['GET'])
def GET_companies():
    with DB.get_cursor() as cursor:
        company_details = list(all_company_details(cursor))
    return {
        'companies': company_details
    }


@app.route('/companies/<cid>', methods=['GET'])
def GET_companies_cid(cid):
    with DB.get_cursor() as cursor:
        company_details = company_details_for_cid(cursor, cid)
        job_details = list(all_job_details_for_cid(cursor, cid))
        hires_by_term = list(hires_by_term_for_cid(cursor, cid))
    return {
        **company_details,
        'jobs': job_details,
        'hires_by_term': hires_by_term,
    }


@ app.route('/jobs', methods=['GET'])
def GET_jobs():
    with DB.get_cursor() as cursor:
        if tag := request.args.get('tag', None):
            job_details = list(all_job_details_for_tag(cursor, tag))
        else:
            job_details = list(all_job_details(cursor))
    return {
        'jobs': job_details
    }


@app.route('/jobs/<jid>', methods=['GET'])
def GET_jobs_jid(jid):
    with DB.get_cursor() as cursor:
        job_details = job_details_for_jid(cursor, jid)
    return job_details


@ app.route('/tags', methods=['GET'])
def GET_tags():
    with DB.get_cursor() as cursor:
        tags = list(all_tags(cursor))
    return {
        'tags': tags
    }


if __name__ == '__main__':
    app.run()
    connection.close()
