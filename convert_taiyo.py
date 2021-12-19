#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob, os, sys, codecs

for filename in glob.iglob("*.xml"):
	with codecs.open(filename, "r", "Shift-JIS", "ignore") as file:
		lines = file.read()
	with codecs.open("u-" + filename, 'w') as file:
		for line in lines:
			file.write(line.encode('utf-8'))