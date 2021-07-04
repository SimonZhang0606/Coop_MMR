import json

from flask import Flask, request, abort
from flask_cors import CORS

from utils.db import DB
from drivers import *


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
        if company_details is None:
            abort(404)
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
        if job_details is None:
            abort(404)
        reviews = list(all_reviews_for_jid(cursor, jid))
        tags = list(all_tags_for_jid(cursor, jid))
    return {
        **job_details,
        'reviews': reviews,
        'tags': tags,
    }


@app.route('/tags', methods=['GET'])
def GET_tags():
    with DB.get_cursor() as cursor:
        tags = list(all_tags(cursor))
    return {
        'tags': tags
    }


if __name__ == '__main__':
    app.run()
    connection.close()
