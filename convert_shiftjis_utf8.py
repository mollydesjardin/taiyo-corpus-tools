# -*- coding: utf-8 -*-

"""
Converts a directory of .xml files (substitute a different extension if needed)
from Shift-JIS encoding to UTF-8, ignoring errors.

This assumes there may be occasional unexpected characters in the input
files, and you would prefer to skip them, read in and convert what you can.
Without the "ignore" argument the script could fail if anything in the
Shift-JIS source files triggers an error.

The output filenams begin with u- to differentiate them and write out to the
same directory.

"""


import glob

for filename in glob.iglob("*.xml"):
	with open(filename, "r", "Shift-JIS", "ignore") as file:
		lines = file.read()
	with open("u-" + filename, 'w') as file:
		for line in lines:
			file.write(line.encode('utf-8'))