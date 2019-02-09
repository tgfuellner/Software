#!/usr/bin/python3

import requests

url = 'http://192.168.0.115:8080/api/v1/status'

print("Content-type: text/html\n")
r = requests.get(url)
stateAll = r.json()

grid = stateAll['GridFeedIn_W']

if grid > -1000 :
	print("build:__green__")
else:
	print("build:__red__")
	
print("<br>eventCount:", grid)
