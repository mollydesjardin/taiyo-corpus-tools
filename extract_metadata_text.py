# -*- coding: utf-8 -*-

"""
global metadata -> year, month or issue number
kiji -> extract metadata (title, author, column, style, genre)

remove <s></s> (not between), odoriji, <br />, <l />, ketsuji and things between, gaiji (not between), inyo
"""


from bs4 import BeautifulSoup as BS
import glob, csv

metadata_keys = ['title', 'author', 'column', 'style', 'genre']

with open('taiyo.csv', 'w', encoding='utf-8') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=metadata_keys)
	writer.writeheader()
    
	# For each file in directory, retrieve file
	for filename in glob.iglob("*.xml"):
		article_prefix = filename[3:-4]

	# Get metadata and write to CSV
		with open(filename, 'r', encoding='utf-8') as soup_in:
			soup = BS(soup_in, "lxml")

			for article in soup('kiji'):
				article_data = {key: article.attrs[key] for key in metadata_keys}
				writer.writerow(article_data)
			
		#save article text
				article_filename = '{}_{}_{}.txt'.format(article_prefix, article_data['author'], article_data['title'])
				if article.ketsuji:
					article.ketsuji.decompose()
				with open(article_filename, 'w', encoding='utf-8') as output_file:
					output_file.write(article.get_text())
