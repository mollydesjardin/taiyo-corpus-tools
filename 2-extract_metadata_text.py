#!/usr/bin/env python3
# -*- coding: utf_8 -*-

# Copyright 2022 Molly Des Jardin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#
# --------------------------------
# Step 2 of Taiyo Corpus Tools
#
# This script reads in XML files containing a monthly magazine issue's worth of # <article>s from NINJAL's Taiyo Corpus, assuming preprocessing by the first
# step of Taiyo Corpus Tools. It saves out article text in individual txt files, 
# and one CSV containing article-level metadata (also including the magazine 
# issue in YYYYMM format).
#
# Output txt files do not contain metadata or other structure, and are not 
# tokenized (no whitespace between words), saved with convention:
#    'data/articles/issue_author_title.txt'
#
# Metadata CSV is saved as 'data/taiyo_metadata.csv'. Columns in order:
#	* articleid (unique ID number per article, padded to 4 digits)
#	* issue (year/month of publication)
#	* title
#	* author
#	* section (欄名)
#	* style (文体)
#	* genre (ジャンル)
#
#
# Tags which are not retained in the metadata, but text between them is retained 
# as part of the article contexts for writing to individual txt file:
#	* s (indicates sentence boundaries)
#	* gaiji (外字)
#	* note (注)
#	* ligature (合字)
#	* quote (引用)
#	* ketsuji (敬意欠字)
#	* odoriji (踊字)
#	* ne (非入力対象)
#
# Tags not retained, that don't enclose any text to retain:
#	* br
#	* l
#
# ("tag removal" is achieved with article.text)

from bs4 import BeautifulSoup as bs
import glob, csv


metadata_keys = ['author','title','section','style','genre']
metadata_list = []
articleid = 0

for infile in glob.iglob("data/utf8/*.xml"):
	with open(infile, 'r', encoding='utf-8') as soup_in:
		soup = bs(soup_in, features="xml")

# Extract month/date of issue (YYYYMM) from filename and retain for metadata CSV
# This is hardcoded to match expected format from Taiyo Corpus Tools step 1.
		issue = infile.split("/")[-1][3:-4]

		for article in soup('article'):
			articleid += 1
			article_md = [str(articleid).zfill(4), issue]
			for key in metadata_keys:
				article_md.append(article.attrs[key])
			metadata_list.append(article_md)
			article_filename = 'data/articles/{}_{}_{}_{}.txt'.format(article_md[0],article_md[1],article_md[2],article_md[3])
			with open(article_filename, 'w', encoding='utf-8') as output_file:
				output_file.write(article.text.strip())

with open('data/taiyo_metadata.csv', 'w', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['articleid', 'issue'] + metadata_keys)
	writer.writerows(metadata_list)
