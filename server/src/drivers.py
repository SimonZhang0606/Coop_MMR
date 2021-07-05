from utils.serialization import serialize_company_details, serialize_job_details, serialize_review, serialize_tag
from queries import *


def all_company_details(cursor):
    cursor.execute(ALL_COMPANY_DETAILS)
    for cd in cursor:
        # print(cd)
        yield serialize_company_details(cd)


def company_details_for_cid(cursor, cid):
    print(cid)
    cursor.execute(COMPANY_DETAILS_FOR_CID, (cid,))
    cd = cursor.fetchone()
    # print(cd)
    return None if cd is None else serialize_company_details(cd)


def all_job_details_for_cid(cursor, cid):
    print(cid)
    cursor.execute(ALL_JOB_DETAILS_FOR_CID, (cid,))
    for jd in cursor:
        # print(jd)
        yield serialize_job_details(jd)


def hires_by_term_for_cid(cursor, cid):
    print(cid)
    cursor.execute(HIRES_BY_TERM_FOR_CID, (cid,))
    for term in cursor:
        # print(term)
        yield {
            'term_num': int(term.term_num),
            'hires': int(term.hires),
        }


def hires_by_term_for_jid(cursor, jid):
    print(jid)
    cursor.execute(HIRES_BY_TERM_FOR_JID, (jid,))
    for term in cursor:
        # print(term)
        yield {
            'term_num': int(term.term_num),
            'hires': int(term.hires),
        }


def all_job_details(cursor):
    cursor.execute(ALL_JOB_DETAILS)
    for jd in cursor:
        # print(jd)
        yield serialize_job_details(jd)


def job_details_for_jid(cursor, jid):
    print(jid)
    cursor.execute(JOB_DETAILS_FOR_JID, (jid,))
    jd = cursor.fetchone()
    # print(jd)
    return None if jd is None else serialize_job_details(jd)


def all_job_details_for_tag(cursor, tag):
    print(tag)
    cursor.execute(ALL_JOB_DETAILS_FOR_TAG, (tag,))
    for jd in cursor:
        # print(jd)
        yield serialize_job_details(jd)


def all_tags(cursor):
    cursor.execute(ALL_TAGS)
    for tag in cursor:
        # print(tag)
        yield serialize_tag(tag)


def all_tags_for_jid(cursor, jid):
    cursor.execute(ALL_TAGS_FOR_JID, (jid,))
    for tag in cursor:
        # print(tag)
        yield serialize_tag(tag)


def all_reviews_for_jid(cursor, jid):
    cursor.execute(ALL_REVIEWS_FOR_JID, (jid,))
    for review in cursor:
        # print(review)
        yield serialize_review(review)


def insert_review_for_jid(cursor, jid, headline, review_body, rating=None):
    cursor.execute(
        INSERT_REVIEW_FOR_JID,
        (headline, review_body, rating, jid,),
    )
    rid = cursor.lastrowid
    cursor.execute(REVIEW_FOR_RID, (rid,))
    review = cursor.fetchone()
    # print(review)
    assert(review is not None)
    return serialize_review(review)
