#!/usr/bin/python

# I live in e.g: /usr/lib/cgi-bin
# showStatus.lua is able to understand what I'm saying

import random

print "Content-type: text/html\n"

if random.randint(1, 2) == 1:
	print("build:__green__")
else:
	print("build:__red__")
	
