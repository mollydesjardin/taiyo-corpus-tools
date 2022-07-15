# Taiyō Corpus Tools
_this doc last updated 8 July, 2022_

## Intro
Taiyō Corpus Tools is a series of short Python scripts that preprocess a corpus of select issues from [Taiyō 太陽 magazine](https://ja.wikipedia.org/wiki/%E5%A4%AA%E9%99%BD_(%E5%8D%9A%E6%96%87%E9%A4%A8) (1895-1928)
 for use with common text analysis tools and software. This edition of the corpus was [released by NINJAL](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) (National Institute for Japanese Language and Linguistics 国立国語研究所) on CD-ROM in 2005. The corpus itself **is not included** here.

The scripts are run as a 3-step pipeline that:
* converts NINJAL's Shift-JIS-encoded, XML files of monthly magazine issues to UTF-8 with romanized tag names;
* strips out XML tags and parses articles into individual text-only files, retaining all article metadata in a separate CSV;
* tokenizes article texts with whitespace between words, using MeCab and a custom dictionary, and saves this final version as article-level .txt files.


### Requirements
* NINJAL Taiyō Corpus data files (see [About the data](#-about-the-data) section below)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [mecab-python3](https://pypi.org/project/mecab-python3/)
* [近代文語UniDic](https://clrd.ninjal.ac.jp/unidic/) (UniDic for Modern Literary Japanese)

## Get started
### Set up your environment
I last debugged and tested this project using Python 3.9 on Mac OS 10.13. You may run into unexpected issues on another setup, but the resources I link to in this readme should be of help if that's the case.

The tokenization step requires mecab-python3 and assumes you have changed your default dictionary to 近代文語UniDic (UniDic for Modern Literary Japanese). See Aurora Tsai's comprehensive [guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798) for very clear instructions for this whole process, covering Mac, Windows, and LinuxBrew.

I chose the Modern Literary Japanese 近代文語 dictionary for tokenization because it most closely matches Taiyō's era and style of language. Using the default UniDic (reflective of 21st-century usage) may not produce the best results because written Japanese has changed so much in relatively recent history. There are a whole range of dictionaries and their documentation at the [UniDic homepage](https://clrd.ninjal.ac.jp/unidic/) so you can choose for yourself. The steps for setting up a custom dictionary for MeCab are the same regardless.

### Get the source data
This repo **does not contain** the data files that the scripts operate on. NINJAL's 2005 CD-ROM edition may still be found on secondary markets if you have no other options and a burning interest.

The Taiyō Corpus is now part of the Meiji/Taishō historical corpora available on NINJAL's Chūnagon 中納言 corpus browser platform (free with registration), but I have not used it myself. Contact NINJAL with any questions about accessing files from them directly.

Some academic libraries in Japan and elsewhere hold this edition of the corpus and lend it via Inter-Library Loan or equivalent (see the [Worldcat entry](http://www.worldcat.org/oclc/191854098) for North American libraries as an example). If you are affiliated with an academic institution, I recommend starting with your librarians for guidance on getting ahold of the CD-ROM. Personally, this is how I got to access this corpus when I was on staff at an American university.

_A version of the Taiyō magazine archives is now available on the JapanKnowledge platform, but is not compatible with these scripts for a whole range of reasons._


## Background
### Why?
[ why was/is Japanese text hard to work with, and it's easier to deal with UTF-8 starting from Python 3 so this used to be more painful in 2.7 when I started this project.

Some steps are common to prepping Japanese text for analysis with tools that assume UTF-8 and/or that your words are separated by spaces.]

### About the data
[explain contents of CD/what I was dealing with ... including INFO links about this particular corpus, plus what is Taiyo at all - all articles from issues in years 1895, 1901, 1909, 1917, 1925. You can find more info about this particular corpus on the [official Taiyo corpus page at NINJAL](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html)]
Notes: it does not cover 100% of the years or articles, but full issues from select years. They can find out more at NINJAL if they want. The disc also includes analysis software that the files are for specific use with but my scripts are for getting the text and select metadata for use with *other* stuff.

(The original XML files are divided by issue and each contain multiple articles. Also, the files themselves have all the metadata embedded in the XML tags/attributes) 

### Why this particular way / my choices
These are a series of very short scripts meant to be run in order and that assume a particular directory structure containing XML files from the NINJAL Taiyō corpus CD-ROM. Each script performs a common task in pre-processing Japanese-language text for use with text analysis software. I kept them separate with the aim of simplifying reuse by others who aren't working with this specific corpus.

These scripts = modular/reusable. They are potentially text processing tasks specific & common to Japanese - encoding conversion, dealing with non-ASCII XML tag names or attributes and why that's a problem for BS, and tokenizing.

I wrote these scripts for my own, one-time personal use, but in an ideal world, they would have command line arguments instead of needing to modify the source to change minor options or put hard-coded configurations in a separate file. I chose a very permissive license for a reason; feel free to adopt and enhance this basic code in your own projects.


## Pipeline
[This is a pipeline meant to be run in a specific order, on specific files that live in specific directory structure. If you're using mine, make the dirs first. Here are some screenshots of what you'd expect to see in Mac Finder of the setup this has been tested on.

[Explain CD-ROM dir structure/file structure I'm assuming first, with screenshots or a little text diagram]

### Step 1: Shift-JIS to Unicode and XML tag names to ASCII
I discovered the hard way that Beautiful Soup (and lxml or similar libraries) don't recognize tag names that aren't ASCII. The Taiyō XML files are full of non-ASCII tags in Japanese, on top of not being UTF-8 encoding.

### Step 2: Extract article text & metadata, write out to untokenized .txt and CSV
This step results in the articles now saved in individual txt files, without tokenization, and writes all the metadata in the stripped XML tags into a CSV to retain. If you want the original Japanese without spaces between "words", stop here (or if you'd like to compare the output of different tokenizer and dictionary choices).

### Step 3: Tokenize article text with MeCab
Have MeCab put a space between "words" in the texts from Step 2. This saves a new set of files rather than overwriting Step 2's output.

## Final output
The final result will be a CSV of all individual articles' metadata extracted from XML tag attributes, and a subfolder of .txt files, one per individual article. Each .txt file contains tokenized UTF-8 plain text contents of one article, and filename is constructed from several fields of metadata separated by underscores. No metadata is placed inside an article text file.

My scripts don't create a unique ID for the articles/files but doing something like issuenumber-001, 002, etc. would be trivial to add to both the CSV rows and filename.

add to "further resources" or in background somewhere


## More Resources
[NINJAL Taiyo Corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html)
[UniDic download & documentation page](https://ccd.ninjal.ac.jp/unidic/en/download_all_en)
[link to my EADH page and eventually "Japanese text analysis FAQ/tutorial" doc if/when I make it. Important or broader links from above for further exploration.](links here)
[guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798)
[J blogpost about wakati / my own posts, as relevant](links)

## Reuse
MIT license (paste info here). Get in touch if you do something cool with this, I'd love to know about it.