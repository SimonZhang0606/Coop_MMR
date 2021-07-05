from linkedin_api import Linkedin
import mysql.connector

from credentials import email, pwd
from usernames import usernames

import random
import uuid
import hashlib
from pprint import pprint
import math

HASH_DIGIT_NUM = 9
TESTING = 1

def random_int_as_str(a, b):
    return str(random.randint(a, b))

def get_uuid():
    return str(uuid.uuid4())

def date_cmp(date1, date2):
    d1 = date1.split("-")
    d2 = date2.split("-")

    if d1[0] > d2[0]:
        return True 
    if d1[0] == d2[0] and d1[1] > d2[1]:
        return True

    return False


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

company_output = []
company_hash = {}
company_elo_hash = {} 

fjob_output = []
fjob_hash = {}

fplacement_output = []
fplacement_hash = {}

matches_result = [] #list of [cid, cid], where the first company is "better" than the next company

placement_tsv = ""


for user_idx, username in enumerate(usernames):

    profile = api.get_profile(username)

    # student
    try:
        student_name = "{} {}".format(profile['firstName'], profile['lastName'])
        sid = hash_string(student_name + random_int_as_str(0, 9), HASH_DIGIT_NUM)
        program = profile['education'][0]['degreeName']
        enrol_date, grad_date = profile['education'][0]['timePeriod']['startDate']['year'], profile['education'][0]['timePeriod']['endDate']['year']
        total_terms = len(profile['experience'])

    except Exception as e:
        print('{}: Missing data for education. Record omitted.'.format(student_name))
        continue

    student_tsv = "{}\t{}\t{}\t{}\t{}\n".format(sid, student_name, program, enrol_date, grad_date)

    fstudent.write(student_tsv)

    omitted_term_count = 0

    match_temp = {} #temperary hash to store the calculations
    

    for i, term in enumerate(profile['experience']):
        try:
            start_year, start_month = term['timePeriod']['startDate']['year'], term['timePeriod']['startDate']['month']

            if enrol_date >= start_year:
                continue
            
            # company
            company_name = term['companyName']
            if company_name not in company_hash:
                cid = hash_string(company_name, HASH_DIGIT_NUM)
                company_hash[company_name] = cid
                company_output.append([cid, company_name])
                company_elo_hash[cid] = [company_name, cid, 1500]

            # job
            job_title = term['title']
            if (job_title, company_name) not in fjob_hash:
                jid = hash_string(str(cid) + job_title, HASH_DIGIT_NUM)
                fjob_hash[(job_title, company_name)] = jid
                fjob_output.append("{}\t{}\t{}\n".format(cid,jid, job_title))

            # placement
            salary = -1 # TODO: determine it later
            
            start_date = str(start_year) + '-' + str(start_month)

            if 'endDate' in term['timePeriod']:
                end_year, end_month = term['timePeriod']['endDate']['year'], term['timePeriod']['endDate']['month']
                end_date = str(end_year) + '-' + str(end_month)
            else:
                end_date = 'N/A'
            
            pid = hash_string(str(cid) + str(jid) + str(sid), HASH_DIGIT_NUM)

            placement_tsv = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cid, jid,  pid, sid,
                            total_terms - omitted_term_count - i, -1, start_date, end_date)

            if company_name not in match_temp:
                for key in match_temp:
                    info = match_temp[key]
                    if date_cmp(start_date, info[1]):
                        matches_result.append([company_name, cid, info[0], info[2]])

                    else: 
                        matches_result.append([info[0], info[2], company_name, cid])
                        
                match_temp[company_name] = [company_name, start_date, cid]
            
        except Exception as e:
            print('{}: Missing data for a job. Job omitted.'.format(student_name))
            
        fplacement.write(placement_tsv)    

#calculate mmr rating 
def Probability(rating1, rating2):
     return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

for match in matches_result:
    c1 = company_elo_hash[match[1]]
    c2 = company_elo_hash[match[3]]

    P2 = Probability(c1[2], c2[2])
    P1 = Probability(c2[2], c1[2])

    mmr_1 = c1[2] + int(50 *(1-P1))
    mmr_2 = c2[2] + int(50 * (0-P2))

    company_elo_hash[match[1]] = [c1[0], c1[1], mmr_1]
    company_elo_hash[match[3]] = [c2[0], c2[1], mmr_2]


for company in company_output:

    company_tsv = "{}\t{}\t{}\n".format(company[0], company[1],company_elo_hash[company[0]][2])
    fcompany.write(company_tsv)


for job_tsv in fjob_output:
    fjob.write(job_tsv)


fcompany.close()
fstudent.close()
fjob.close()
fplacement.close()




