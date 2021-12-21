# -*- coding: utf-8 -*-

"""
This script reads in each XML file containing an issue's worth of articles from
the Taiyo magazine CD-ROM published by NINJAL, in the XML directory on the CD.
The input filenames contain year/month (ex. t189501.xml = January 1895). Other
metadata per-article is retrieved from attributes in the "kiji" tag which
indicates start/end of each article.
Output is a plain text file, with no XML tags and no tokenization (whitespace)
inserted between words, with filename convention:
    year/date_author_title
And a CSV file containing all metadata per-article:

per file: year, month of issue (from filename)
per article tag within file: title, author, column, style, genre

Other cleanup...
remove tags/attrs but retain text enclosed between:
s, gaiji (外字), chu (注), ligature (合字), quote (引用), ketsuji (敬意欠字), odoriji (踊字)
remove tags that don't enclose any text: br, l
(because no tags need to have text between them removed, this is all achieved
 with article.text)

"""


from bs4 import BeautifulSoup as BS
import glob, csv

metadata_keys = ['author','title','column','style','genre']
articles_list = []
    
for infile in glob.iglob("*.xml"):
# Get metadata and put in dict. Write out file with text only as cleaned
    with open(infile, 'r', encoding='utf-8') as soup_in:
        soup = BS(soup_in, 'lxml')
        issuedate = infile[3:-4]

# saving metadata for writing out later
        for article in soup('article'):
            article_md = []
            article_md.append(issuedate)
            for key in metadata_keys:
                article_md.append(article.attrs[key])
            articles_list.append(article_md)

            article_filename = 'articles/{}_{}_{}.txt'.format(article_md[0], article_md[1], article_md[2])

            with open(article_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(article.text.strip())

# write header from metadata_keys then write each row of md in list
with open('taiyo_metadata.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['issue'] + metadata_keys)
    writer.writerows(articles_list)
