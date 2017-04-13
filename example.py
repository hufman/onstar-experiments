#!/usr/bin/env python

from os.path import expanduser
from getpass import getpass
import pprint
pp = pprint.PrettyPrinter(indent=4)

# save login cookies between runs
from http.cookiejar import LWPCookieJar, DefaultCookiePolicy
DefaultCookiePolicy.DEBUG = 1
cookies = LWPCookieJar(expanduser('onstar.cookies'))
try:
	cookies.load(ignore_discard=True, ignore_expires=True)
except IOError:
	cookies.save()


# prompt for auth creds
username = input('Username: ')
password = getpass('Password: ')

# try to login
from onstar.client import OnStarClient
client = OnStarClient(username, password, cookies)

# save login cookies
cookies.save(ignore_discard=True, ignore_expires=True)

# load data
cars = client.get_garage()
print("Discovered cars:")
pp.pprint(cars)
electric_cars = [c for c in cars if 'Electric' in c['fuelType']]
for car in electric_cars:
	print("Fetching data via OnStar from %s %s %s:" % (car['year'], car['make'], car['model']))
	pp.pprint(car.get_evstats())
