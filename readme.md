# Taiyō Corpus Tools
_this doc last updated 21 September, 2022_

## Intro
Taiyō Corpus Tools is a set of short Python scripts that preprocesses Japanese-language text from [NINJAL's Taiyō Corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) for use with common text analysis software. The steps consist of:
 
1. convert_shiftjis_utf8.py -- convert NINJAL's Shift-JIS-encoded, XML files of monthly magazine issues to UTF-8 with romanized XML tag names
2. extract_metadata_text.py -- strip out XML tags and parses articles into individual text files; save corresponding article metadata in a separate CSV
3. tokenize.py -- insert whitespace between words using MeCab and save final output as article-level .txt files

### Requirements
* NINJAL Taiyō Corpus data files (see [About the data](#-about-the-data) section below)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [mecab-python3](https://pypi.org/project/mecab-python3/)
* [近代文語UniDic](https://clrd.ninjal.ac.jp/unidic/) (UniDic for Modern Literary Japanese, suggested)

## Get started
### Set up your environment
I last debugged and tested this project using Python 3.9 on Mac OS 10.13. You may run into unexpected issues on another setup, but further resources linked throughout this document should be of help.

The tokenization step requires mecab-python3 and assumes you have changed your default dictionary to 近代文語UniDic (UniDic for Modern Literary Japanese). See Aurora Tsai's comprehensive [guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798) for very clear instructions for this whole process for multiple systems (Mac, Windows, and LinuxBrew).

Using the Modern Literary Japanese 近代文語 dictionary is optional, but it most closely matches Taiyō's era and style of language and should produce the best word-splitting results. There are a whole range of dictionaries and their documentation at the [UniDic homepage](https://clrd.ninjal.ac.jp/unidic/). Of course, if you decide to use the default dictionary you can skip the customization step.

### Get the source data
This repo **does not contain** the data files that make up NINJAL's corpus. Their [2005 CD-ROM edition](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) may still be found on secondary markets if you wish to purchase your own copy. Other suggestions below from my former life as an academic librarian.

The Taiyō Corpus is now part of the Meiji/Taishō historical corpora available on NINJAL's Chūnagon 中納言 corpus browser platform (free with registration), but I don't know if data download is possible or in similar format to the CD-ROM's files. Contact NINJAL with any questions about accessing data from them directly.

Some university libraries in Japan and elsewhere own the CD-ROMs and lend it via Inter-Library Loan or equivalent (see the [Worldcat entry](http://www.worldcat.org/oclc/191854098) for North American libraries). If you are affiliated with an academic institution, ask your library for guidance.

_A version of the Taiyō magazine archives is lately available on the JapanKnowledge platform, which some universities license. It is **not compatible** with these scripts, not least because it doesn't contain article full-text._


## Background
### Why?
The tasks performed by these three scripts are common ones for making Japanese-language text files compatible with NLP software. Typically, non-Japanese-specific tools assume whitespace tokenization or UTF-8 encoding. Additionally, Beautiful Soup and other XML/HTML parsing libraries cannot handle non-ASCII tag or attribute names, as found in the NINJAL Taiyō files (as of this writing). None of the issues with these files is unique to the NINJAL corpus or data prepared by NINJAL generally. You may encounter specialized encoding or seemingly quirky technical aspects in any Japanse text documents, especially if they are "older" (relatively speaking). My description applies to the _vast majority_ of what you might find as source material for text analysis projects online in Japanese, even in 2022, in fields ranging from literature to law and government. However, this mismatch of source and software is solvable.

My motivation was personal: I wanted to try using the Taiyō articles with software popular among digital humanities enthusiasts, like Voyant, AntConc, or Topic Modeling Tool. I also wanted to be able to show the possibilities to colleagues in academic librarianship or university Japanese studies programs through demos and workshops. However, "having" texts in some machine-readable format doesn't mean they are necessarily compatible with the widespread assumptions of DH tools outside Japan. It is the start but often not the end.

Short and simple as it looks now, when I began grappling with Taiyō around 2015, I was still using Python 2.7 and there was little to no documentation online (in any language I read) that really addressed what I was attempting to do. I spent a long time searching online and reading Japanese or English blog posts about barely-referenced options for MeCab, cobbling tidbits from various sources together to eventually solve my problem: a MeCab parsing option that was compatible with the dictionary I needed to use; getting around non-ASCII XML tags breaking the libraries I tried to parse them; and dealing with the niche encoding. (I got some invaluable advice from colleagues as well.) In 2022, some of the issues are either much more searchable online, or no longer exist in Python 3 -- especially re: Unicode data, bane of my existence in 2.7.

I am very pleased to no longer be hitting my head against the wall of ancient Python "handling" of Unicode (etc), but some things that now seem obvious to me may still not be straightforward to others. I hope documenting my process, and sharing the code, can save someone else from doing the same with their own annoying barrier to research with historical Japanese texts.

### About the data
NINJAL's Taiyō Corpus is a subset of full-text, hand-corrected articles from [Taiyō 太陽 magazine](https://ja.wikipedia.org/wiki/%E5%A4%AA%E9%99%BD_(%E5%8D%9A%E6%96%87%E9%A4%A8) (1895-1928). The contents of the corpus include all articles from issues published in 1895, 1901, 1909, 1917, 1925. While it is a large amount of text, it doesn't cover the magazine's run comprehensively. You can find more info about this particular corpus on the [official Taiyo corpus page at NINJAL](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html). Although the CD-ROM edition includes the Himawari software for corpus analysis, the scripts I provide here are meant for getting the text and select metadata usable with any *other* tools -- especially those that are not meant specifically for Japanese language.

The data consists of one XML file per magazine issue containing all articles' text and metadata. The corpus is hand-corrected full-text annotated by professional linguists -- very high quality, and far better than OCR alone given its poor performance on Japanese documents of this period and format. All metadata is contained within the XML tags in the data files: publishing information for the magazine issues and each article (author, title, genre) and specialized linguistic attributes at the article or word level (style of speech, and glosses of errors or rare kanji that could not be entered at the time). There is tokenization of the articles themselves but only at the sentence level.

### Why this particular way / my choices
Each script in this pipeline performs a very simple task, but I have kept them separate to simplify reuse by others who aren't working with this specific corpus. They are potentially text processing tasks specific & common to Japanese - encoding conversion, dealing with non-ASCII XML tag names or attributes and why that's a problem for BS, and tokenizing.
These scripts = modular/reusable. 


## Pipeline
[This is a pipeline meant to be run in a specific order, on specific files that live in specific directory structure. If you're using mine, make the dirs first. 

### Directory structure
[this is presented as files, then directories in alphabetical order]
Taiyo/
|-- convert_shiftjis_utf8.py
|-- extract_metadata_text.py
|-- tokenize.py
`-- data/
    |-- taiyo_metadata.csv //output of extract_metadata_text.py
    |-- articles/
    |   |-- //output of extract_metadata_text.py
    |   |-- 189501_＊_〈扉〉.txt
    |   |-- 189501_＊_〈新年挨拶〉.txt
    |   |-- ...
    |   |-- 192514_金易二郎（出題）_詰将棋新題.txt
    |   |-- 192514_金易二郎（評）_高段名手　特選将棋.txt
    |   `-- 192514_鬼谷庵_政界鬼語.txt
    |-- taiyo_cd/
    |   |-- //directory structure on CD-ROM of relevant XML files
    |   |-- autorun.inf
    |   |-- Himawari/
    |   |-- index.html
    |   |-- license.txt
    |   |-- taiyo.ico
    |   `-- XML/
    |       |-- t189501.xml
    |       |-- t189502.xml
    |       |-- t189503.xml
    |       |-- ...
    |       `-- t192514.xml
    |-- tokenized/
    |   |-- //output of tokenize.py
    |   |-- t-189501_＊_〈扉〉.txt
    |   |-- t-189501_＊_〈新年挨拶〉.txt
    |   |-- ...
    |   |-- t-192514_金易二郎（出題）_詰将棋新題.txt
    |   |-- t-192514_金易二郎（評）_高段名手　特選将棋.txt
    |   `-- t-192514_鬼谷庵_政界鬼語.txt
    `-- utf8/
        |-- //output of convert_shiftjis_utf8.py
        |-- u-t189501.xml
        |-- u-t189502.xml
        |-- ...
        `-- u-t192514.xml

### Step 1: Shift-JIS to Unicode and XML tag names to ASCII
Beautiful Soup don't recognize tag names that aren't ASCII. The Taiyō XML files are full of non-ASCII tags in Japanese, on top of not being UTF-8 encoding.

### Step 2: Extract article text & metadata, write out to untokenized .txt and CSV
This step results in the articles now saved in individual txt files, without tokenization, and writes all the metadata in the stripped XML tags into a CSV to retain. If you want the original Japanese without spaces between "words", stop here (or if you'd like to compare the output of different tokenizer and dictionary choices).

### Step 3: Tokenize article text with MeCab
Have MeCab put a space between "words" in the texts from Step 2. This saves a new set of files rather than overwriting Step 2's output.

## Final output
Then your output will be X Y relative to the directory where you ran them. (where is it, what are the files called... concretely)
Also explain the filename convention and that you can/should change it to what you prefer. Make sure you modify the CSV output to include a unique ID index column if you decide to do that.



## Further Resources
[NINJAL Taiyo Corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html)
[UniDic download & documentation page](https://ccd.ninjal.ac.jp/unidic/en/download_all_en)
[guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798)
[J blogpost about wakati](link)
[my own old post(s) about Taiyo, as relevant](links)
[Japanese NLP posts by Paul O'Leary McCann @ Dampfkraft](https://www.dampfkraft.com/nlp.html)


## Reuse
Copyright Molly Des Jardin

I wrote these scripts for my own, one-time personal use, and no longer maintain them. Ideally, I would prefer command line arguments and/or a config file instead of so much hard-coding throughout. There are doubtless other changes that might improve the code or design. I chose a very permissive license for a reason: please freely adopt and enhance this basic code in your own projects.


MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.