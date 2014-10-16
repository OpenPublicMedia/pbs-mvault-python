#!/usr/bin/env python
"""
Example script to parse a CSV file and ingest the member record.

By: Rob Vincent <rvincent@opb.org>, Oregon Public Broadcasting
Created: October 1, 2014

"""
import sys
import csv
import pytz
from datetime import datetime

from mvault import Vault, Member
from config import CALLSIGN, KEY, SECRET


if len(sys.argv) < 2:
	print("usage: %s <member file>" % sys.argv[0])
	sys.exit(1)

vault = Vault(CALLSIGN, KEY, SECRET)
tz = pytz.timezone('US/Pacific')

with open(sys.argv[1], 'rb') as csvfile:
	member_reader = csv.reader(csvfile, delimiter='\t')
	next(member_reader)	# skip header row
	for row in member_reader:
		member = Member()
		member.parse({
			'first_name': row[0],
			'last_name': row[1],
			'offer': row[2],
			'membership_id': row[3],
			'start_date': tz.localize(datetime.strptime(row[4], '%m/%d/%Y')),
			'expire_date': tz.localize(datetime.strptime(row[5], '%m/%d/%Y')),
			'email': row[6],
			'status': 'On'
		})
		vault.membership_update(member)
