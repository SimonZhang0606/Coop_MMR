from linkedin_api import Linkedin
import mysql.connector

from credentials import email, pwd
from usernames import usernames

import uuid
import hashlib
from pprint import pprint

HASH_DIGIT_NUM = 9

def get_uuid():
    return str(uuid.uuid4())


def connect_mysql():
    mydb = mysql.connector.connect(host=MYSQL_HOST,
                                   user=MYSQL_USER,
                                   passwd=MYSQL_PWD,
                                   database=MYSQL_DB_NAME)
    return mydb


def insert_student(name, term_data):
    insert_command = 'INSERT INTO {0} (PID, SID, CID, Title, StartMonth, StartYear, EndMonth, EndYear'.format(
        TABLE_NAME)

def hash_string(s, digit_num):
    r = str(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10 ** digit_num)
    
    while (len(r) < digit_num):
        r = '0' + r

    return r

api = Linkedin(email, pwd)


fcompany = open("data/company.tsv", "a")
fjob = open("data/job.tsv", "a")
fstudent = open("data/student.tsv", "a")
fplacement = open("data/placement.tsv", "a")

for user_idx, username in enumerate(usernames):
    profile = api.get_profile(username)
    # pprint(profile)

    # student
    try:
        student_name = "{} {}".format(profile['firstName'], profile['lastName'])
        sid = hash_string(student_name, HASH_DIGIT_NUM)
        program = profile['education'][0]['degreeName']
        enrol_date, grad_date = profile['education'][0]['timePeriod']['startDate']['year'], profile['education'][0]['timePeriod']['endDate']['year']
        total_terms = len(profile['experience'])
    except Exception as e:
        print('{}: Missing data for education. Record omitted.'.format(student_name))
        continue

    student_tsv = "{}\t{}\t{}\t{}\t{}\n".format(sid, student_name, program, enrol_date, grad_date)

    fstudent.write(student_tsv)

    omitted_term_count = 0
    
    for i, term in enumerate(profile['experience']):
        try:
            start_year, start_month = term['timePeriod']['startDate']['year'], term['timePeriod']['startDate']['month']

            if enrol_date >= start_year:
                continue

            # company
            company_name = term['companyName']
            cid = hash_string(company_name, HASH_DIGIT_NUM)
            company_tsv = "{}\t{}\n".format(cid, company_name)

            # job
            job_title = term['title']
            jid = hash_string(str(cid) + job_title, HASH_DIGIT_NUM)
            job_tsv = "{}\t{}\t{}\t{}\n".format(cid, jid, 1500, job_title)

            # placement
            salary = -1 # TODO: determine it later
            
            start_date = str(start_year) + '-' + str(start_month)

            if 'endDate' in term['timePeriod']:
                end_year, end_month = term['timePeriod']['endDate']['year'], term['timePeriod']['endDate']['month']
                end_date = str(end_year) + '-' + str(end_month)
            else:
                end_date = 'N/A'
            
            pid = hash_string(str(cid) + str(jid) + str(sid), HASH_DIGIT_NUM)

            placement_tsv = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cid, jid, pid, sid, 
                            total_terms - omitted_term_count - i, -1, start_date, end_date)
        except Exception as e:
            print('{}: Missing data for a job. Job omitted.'.format(student_name))
            continue
        
        fcompany.write(company_tsv)
        fjob.write(job_tsv)
        fplacement.write(placement_tsv)

fcompany.close()
fstudent.close()
fjob.close()
fplacement.close()
