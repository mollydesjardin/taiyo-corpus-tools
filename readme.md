# Taiyo corpus tools
_this doc last updated..._

## Intro
[short explanation of the project; dependencies = BeautifulSoup 4, mecab-python3 & assumes 近代文語UniDic (UniDic for Modern Literary Japanese) is being used in tokenization step, but this must be customized on your own system; last debugged & tested with Python 3.9 on Mac OS 10.13 specifically. Use one sentence of "WHY" in background section below to set up the project.]

## Get started
These are a series of very short scripts meant to be run in order and that assume a particular directory structure containing XML files from the NINJAL Taiyō corpus CD-ROM. (See the "How to use pipeline" section for step-by-step details.)

Each script performs a common task in pre-processing Japanese-language text for use with text analysis software. I kept them separate with the aim of simplifying reuse by others who aren't working with this specific corpus.

In order to run the scripts, you will need to install BeautifulSoup 4, and they were tested running Python 3.9 on MacOS. The tokenization step requires mecab-python3 and assumes 近代文語UniDic (UniDic for Modern Literary Japanese) is being used. See this detailed [guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798) for the latter.

Note that this repo does NOT contain any corpus (source text) files, which are not in the public domain. NINJAL packaged and sold the files and analysis software, with added linguistic annotations, on CD-ROM in 2005. Some academic libraries hold this edition of the corpus and may lend it via Inter-Library Loan  or equivalent (see the [Worldcat entry](http://www.worldcat.org/oclc/191854098) for in the US as an example). For access to NINJAL's CD-ROM edition texts, I recommend starting with your university librarian or contacting NINJAL directly for guidance.

Side note: Taiyō magazine archives are also licensed through the academic database JapanKnowledge, and this edition is NOT compatible with the scripts here. This project assumes you are working with NINJAL's annotated XML files.


## Background
[Including links about this particular corpus, plus what is Taiyo at all - all articles from issues in years 1895, 1901, 1909, 1917, 1925. You can find more info about this particular corpus on the [official Taiyo corpus page at NINJAL](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) Also, why was/is Japanese text hard to work with, and it's easier to deal with UTF-8 starting from Python 3 so this used to be more painful in 2.7 when I started this project.

Some steps are common to prepping Japanese text for analysis with tools that assume UTF-8 and/or that your words are separated by spaces.

note but in a less wordy way: Link to NINJAL CD/DVD record in Worldcat and their site for ref; note clearly that "if you have access to Taiyo magazine via Japan Knowledge at your institution, it is COMPLETELY DIFFERENT from this and is not the source file(s) -- you need the disc specifically because it contains XML files that are hand-corrected and annotated, selected transcriptions by linguists at NINJAL." Also that it does not cover 100% of the years or articles, but full issues from select years. They can find out more at NINJAL if they want. The disc also includes analysis software that the files are for specific use with but my scripts are for getting the text and select metadata for use with *other* stuff.

WHY is this needed/ why even do this, and why are these scripts modular/reusable? basically what potentially common text processing tasks are they doing and specific to Japanese - encoding conversion, dealing with non-ASCII XML tag names or attributes and why that's a problem for BS, and tokenizing. This isn't a guide to MeCab installation or usage, link to some other resources on both of those (including the wakati blogpost I used originally). Note you'll want to use a different dictionary from default due to the language in Taiyo, which will always vary depending on the content of what you're working with -- you can experiment with this too and see if you agree with its decisions depending on your dictionary. Link out to [UniDic download & documentation page](https://ccd.ninjal.ac.jp/unidic/en/download_all_en)

## How to Use Pipeline
[This is a pipeline meant to be run in a specific order, on specific files that live in specific directory structure. If you're using mine, make the dirs first. Here are some screenshots of what you'd expect to see in Mac Finder of the setup this has been tested on.

### Step 1: Shift-JIS to Unicode and XML tag names to ASCII

### Step 2: Extract article text & metadata, write out to untokenized .txt and CSV

### Step 3: Tokenize article text with MeCab

## Final output
The final result will be a CSV of all individual articles' metadata extracted from XML tag attributes, and a folder of .txt files, one per individual article. (The original XML files are divided by issue and each contain multiple articles.) Each .txt file contains tokenized UTF-8 plain text contents of one article, and filename is constructed from several fields of metadata separated by underscores. No metadata is placed inside an article text file (see the CSV for full set of metadata per article).

My scripts don't create a unique ID for the articles/files but doing something like issuenumber-001, 002, etc. would be trivial to add to both the CSV rows and filename.]


## More Resources
[link to my EADH page and eventually "Japanese text analysis FAQ/tutorial" doc if I make it. And/or repeat links from above as roundup of further exploration.]


## Reuse
[This is released to the public domain with a CC-0 dedication. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. See the [human-readable summary of CC0 1.0 Universal Public Domain Declaration](https://creativecommons.org/publicdomain/zero/1.0/) for more. There are some hypothetical issues with patent rights involving CC-0 for source code but after spending more time than is justified researching my options, I couldn't find a better solution as of early 2022.]