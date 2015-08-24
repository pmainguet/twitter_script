#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use Twitter API to grab user information from list of organizations; 
export text file
Uses Twython module to access Twitter API
"""
import csv
import sys
import string
import simplejson
from twython import Twython

#WE WILL USE THE VARIABLES DAY, MONTH, AND YEAR FOR OUR OUTPUT FILE NAME
import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)


#FOR OAUTH AUTHENTICATION -- NEEDED TO ACCESS THE TWITTER API
t = Twython(app_key='5HeBOrYw4NpLLSTSBNizTIrXe', #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret='0frgT45TSKtNFZrIptXFs0ENWRUbANfDqevI9hudeUPOpnqeRL',
    oauth_token='127840133-7sVWM3NgWXSpnGPcniKn645DHCUUz6R9O0rLxeOB',
    oauth_token_secret='MdEb6NlaRqeGarBob7VY7QbQ3W93vJNcfzXlfUD2jhkqf')
   
#NAME OUR OUTPUT FILE - %i WILL BE REPLACED BY CURRENT MONTH, DAY, AND YEAR
outfn = "twitter_user_data_%i.%i.%i.csv" % (now.month, now.day, now.year)

#NAMES FOR HEADER ROW IN OUTPUT FILE
fields = ["id","screen_name","name","created_at","url","followers_count","description","location"]

#INITIALIZE OUTPUT FILE AND WRITE HEADER ROW 
outfp = csv.writer(open(outfn, "wb"))
outfp.writerow(fields)

#REPLACE WITH YOUR LIST OF TWITTER USER IDS

with open('twitter_following2.csv', 'rb') as csvfile:

	row_count = sum(1 for row in csvfile)-1
	quotient=row_count/100
	reste=row_count-quotient*100

	print(row_count)
	
	if reste!=0:
		last_range=quotient+1
	else:
		last_range=quotient

	for i in range(1,last_range+1):
		ids=''	
		count_init=1+(i-1)*100
		count_last=i*100
		if count_last > row_count:
			count_last=row_count
		count=0

		csvfile.seek(0)

		print("Process "+str(count_init)+" to "+str(count_last)+" out of "+str(row_count))
		
		for row in csv.reader(csvfile):
			if count >=count_init and count <=count_last:
				ids+=row[0]+","
			count+=1

		#ACCESS THE LOOKUP_USER METHOD OF THE TWITTER API -- GRAB INFO ON UP TO 100 IDS WITH EACH API CALL
		#THE VARIABLE USERS IS A JSON FILE WITH DATA ON THE 32 TWITTER USERS LISTED ABOVE
		users = t.lookup_user(user_id = ids)

		#THE VARIABLE 'USERS' CONTAINS INFORMATION OF THE 32 TWITTER USER IDS LISTED ABOVE
		#THIS BLOCK WILL LOOP OVER EACH OF THESE IDS, CREATE VARIABLES, AND OUTPUT TO FILE
		for entry in users:
		    row=[]
		    for f in fields:
			row.append(entry[f])
		    outfp.writerow([unicode(s).encode("utf-8") for s in row])
print("Done!")
