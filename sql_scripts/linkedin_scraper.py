from hashlib import sha256
import math

from linkedin_api import Linkedin

from credentials import email, pwd
from usernames import usernames


def date_cmp(date1, date2):
    d1 = date1.split("-")
    d2 = date2.split("-")

    if d1[0] > d2[0]:
        return True
    if d1[0] == d2[0] and d1[1] > d2[1]:
        return True

    return False


def hash_string(s):
    return int(sha256(s.encode('utf-8')).hexdigest(), 16)


def format_date(year, month=1, day=1):
    return f'{year:04}-{month:02}-{day:02}'


class IDFactory:
    def __init__(self):
        self.used_ids = set()

    def __call__(self, s, length=9):
        base = 10**length
        hashed = hash_string(s) % base
        while hashed in self.used_ids:
            hashed = (hashed+1) % base
        self.used_ids.add(hashed)
        return f'{hashed:0{length}}'

make_cid = IDFactory()
make_jid = IDFactory()
make_pid = IDFactory()
make_sid = IDFactory()


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

matches_result = [] # list of [cid, cid], where the first company is "better" than the next company

placement_tsv = ""


for username in usernames:

    profile = api.get_profile(username)

    # student
    try:
        student_name = "{} {}".format(profile['firstName'], profile['lastName'])
        sid = make_sid(student_name)
        program = profile['education'][0]['degreeName']
        enrol_date, grad_date = profile['education'][0]['timePeriod']['startDate']['year'], profile['education'][0]['timePeriod']['endDate']['year']
        total_terms = len(profile['experience'])

    except Exception as e:
        print('{}: Missing data for education. Record omitted.'.format(student_name))
        continue

    student_tsv = "{}\t{}\t{}\t{}\t{}\n".format(sid, student_name, program, enrol_date, grad_date)

    fstudent.write(student_tsv)

    omitted_term_count = 0

    match_temp = {} # temporary hash to store the calculations


    for i, term in enumerate(profile['experience']):
        try:
            start_year, start_month = term['timePeriod']['startDate']['year'], term['timePeriod']['startDate']['month']
            if enrol_date >= start_year:
                continue
            start_date = format_date(year=start_year, month=start_month)

            if 'endDate' in term['timePeriod']:
                end_year, end_month = term['timePeriod']['endDate']['year'], term['timePeriod']['endDate']['month']
                if grad_date < end_year:
                    continue
                end_date = format_date(year=end_year, month=end_month)
            else:
                end_date = 'N/A'

            # company
            company_name = term['companyName']
            if company_name in company_hash:
                cid = company_hash[company_name]
            else:
                cid = make_cid(company_name)
                company_hash[company_name] = cid
                company_output.append([cid, company_name])
                company_elo_hash[cid] = [company_name, cid, 1500]

            # job
            job_title = term['title']
            if (job_title, company_name) in fjob_hash:
                jid = fjob_hash[(job_title, company_name)]
            else:
                jid = make_jid(str(cid) + job_title)
                fjob_hash[(job_title, company_name)] = jid
                fjob_output.append("{}\t{}\t{}\n".format(cid, jid, job_title))

            # placement
            salary = -1 # TODO: determine it later

            pid = make_pid(str(cid) + str(jid) + str(sid) + start_date)

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


# calculate mmr rating
def Probability(rating1, rating2):
    return 1. / (1. + math.pow(10., (rating1 - rating2) / 400.))

for match in matches_result:
    c1 = company_elo_hash[match[1]]
    c2 = company_elo_hash[match[3]]

    P2 = Probability(c1[2], c2[2])
    P1 = Probability(c2[2], c1[2])

    mmr_1 = c1[2] + int(50 * (1-P1))
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
