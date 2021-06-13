from linkedin_api import Linkedin 
from credentials import email, pwd
import mysql.connector

import uuid

from pprint import pprint

TABLE_NAME = 'STUDENT'

def get_uuid():
    return str(uuid.uuid4())

def connect_mysql():
    mydb = mysql.connector.connect(host=MYSQL_HOST, 
                                    user=MYSQL_USER, 
                                    passwd=MYSQL_PWD,
                                    database=MYSQL_DB_NAME)
    return mydb

def insert_student(name, term_data):
	insert_command = 'INSERT INTO {0} (PID, SID, CID, Title, StartMonth, StartYear, EndMonth, EndYear'.format(TABLE_NAME)


api = Linkedin(email, pwd)

usernames = ['beinifang', 'julia-youlin-du', 'thelindazheng', 'edwardhdlu',
			'jeff-luo', 'bharatt-kukreja', 'dennis-qin-75bb8b130', 'yucheng-yan-22a273b1', 
			'ericrfeng', 'jason17huang', 'diantang', 'jackie-xu', 'xujustinj',
			'kelvin-zhang', 'athena-liu', 'anushkabirla', 'siddharth-kumar', 'alan-cl-wu',
			'shiyi-peng', 'dev-pancea-018b7116a', 'cindywang328', 'anna-lok']

for username in usernames:
	profile = api.get_profile(username)
	# pprint(profile)

	experience = []
	for term in profile['experience']:

		term_data = [term['companyName'], term['title'], term['timePeriod']]
		



