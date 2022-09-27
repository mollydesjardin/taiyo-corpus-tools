# Taiyō Corpus Tools
_last updated 27 September, 2022_

## Intro
Taiyō Corpus Tools is a set of short Python scripts that preprocesses Japanese-language text from [NINJAL's Taiyō 太陽 magazine corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) for use with common analysis software. Run the three scripts in order:

* 1-convert_shiftjis_utf8.py -- convert NINJAL's Shift-JIS-encoded, XML files of monthly magazine issues to UTF-8 with ASCII XML tags/attributes

* 2-extract_metadata_text.py -- export article text content only to individual files; save article-level metadata from XML tags to single CSV

* 3-tokenize.py -- insert whitespace between words in article text using MeCab and save final output as individual, tokenized text files

### Requirements
* NINJAL Taiyō Corpus data files (see [Get the source data](#get-the-source-data) below)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [mecab-python3](https://pypi.org/project/mecab-python3/)
* [近代文語UniDic](https://clrd.ninjal.ac.jp/unidic/) (UniDic for Modern Literary Japanese, suggested)
* Configure MeCab to use non-default dictionary

## Get started
### Set up your environment
Tokenization requires mecab-python3 and assumes you have changed your default dictionary to 近代文語UniDic (UniDic for Modern Literary Japanese). See Aurora Tsai's comprehensive [guide to installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798) for very clear instructions on multiple systems (Mac, Windows, and LinuxBrew).

Using the 近代文語UniDic is optional, but it most closely matches Taiyō's era and style of language and should produce the best word-splitting results. There are a whole range of dictionaries and their documentation at the [UniDic homepage](https://clrd.ninjal.ac.jp/unidic/).

### Directory structure
All three scripts assume the following directory structure relative to themselves.

*Before running the scripts, make sure expected directories exist within "data/" folder: articles, tokenized, utf8.* Each script saves output separately without overwriting previous files. "data/taiyo_cd/" indicates the corpus CD-ROM data, not included here.

```
Taiyo/
|-- 1-convert_shiftjis_utf8.py
|-- 2-extract_metadata_text.py
|-- 3-tokenize.py
`-- data/
    |-- taiyo_metadata.csv
    |-- articles/
    |   |-- 0001_190103_＊_〈扉〉.txt
    |   |-- 0002_190103_＊_憲政の一大危機.txt
    |   |-- 0003_190103_肥塚龍_支那保全と満州処分.txt
    |   |-- ...
    |-- taiyo_cd/
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
    |   |-- t-0001_190103_＊_〈扉〉.txt
    |   |-- t-0002_190103_＊_憲政の一大危機.txt
    |   |-- t-0003_190103_肥塚龍_支那保全と満州処分.txt
    |   |-- ...
    `-- utf8/
        |-- u-t189501.xml
        |-- u-t189502.xml
        |-- ...
        `-- u-t192514.xml
```

### Get the source data
This repo **does not contain** the data files that make up NINJAL's corpus. I assume the contents of "data/taiyo_cd/" is a copy of the [2005 CD-ROM edition](http://www.hakubunkan.co.jp/gengo/taiyoC.html). It may still be purchased on secondary markets, but below are some other suggestions on getting the text data.

The Taiyō Corpus is now part of the [Meiji/Taishō historical corpora](https://clrd.ninjal.ac.jp/chj/meiji_taisho.html) available on NINJAL's Chūnagon 中納言 corpus browser platform (free with registration), but access to the full dataset probably requires contacting them directly.

Some university libraries own the CD-ROMs and lend it via Inter-Library Loan or equivalent (see the [Worldcat entry](http://www.worldcat.org/oclc/191854098) for an example). If you are affiliated with a university, ask your librarian for guidance.

_A version of the Taiyō magazine archives is also available on the JapanKnowledge platform, which some universities license. It is **not compatible** with these scripts._


## Background
### Why?
Short and simple as it looks now, when I started trying to work with NINJAL's Taiyō Corpus in 2015, I could find almost no documentation that really addressed the issues I ran into. Because I was still using Python 2.7 at the time, dealing with documents encoded with UTF-8 or Shift-JIS was also much more of a struggle.

I spent a long time searching online and reading Japanese or English blog posts that were mainly about something else, cobbling together a solution to my issues with tidbits from various tangential sources. (I got some invaluable tips on MeCab configuration directly from [Mark Ravina](https://liberalarts.utexas.edu/history/faculty/mr56267) as well.)

In 2022, some of the problems I encountered have solutions readily searchable online, or even better, no longer exist. But "quirky" issues like the ones here are still common with Japanese-language documents, and not unique to Taiyō. I hope documenting my process, and sharing the code, can save others some time and frustration.

### About the data
NINJAL's Taiyō Corpus contains full-text, hand-corrected articles from [Taiyō 太陽 magazine](https://ja.wikipedia.org/wiki/%E5%A4%AA%E9%99%BD_%28%E5%8D%9A%E6%96%87%E9%A4%A8%29) (published 1895-1928). The corpus includes thousands of articles from 1895, 1901, 1909, 1917, and 1925. You can find more info about this particular corpus on [NINJAL's website](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html).

The dataset consists of one XML file per magazine issue, with both text and metadata. The article text is hand-corrected and annotated with linguistic data at the word level, so the quality is much better than OCR on documents from this time/language. Metadata in the XML tags includes:
- publishing information for the magazine issues
- publishing information for each article (author, title, genre)
- specialized linguistic attributes at the article or word level (style of speech, and glosses of errors or rare kanji that could not be entered at the time).

Article text is tokenized at the sentence level only.

## Running the scripts
All three scripts operate assuming the [directory structure and files described above](#directory-structure). They should be run in the top-level project directory with no arguments.

### Step 1: Shift-JIS to Unicode and XML normalization
The Taiyō XML files contain many XML elements and attributes named in Japanese. While this is valid XML, it presents a problem for parsing libraries (as of this writing). This script replaces all non-ASCII tag and element names with romanized or English keyword equivalents. Output is saved as one UTF-8 .xml file per magazine issue, in directory "data/utf8/" with u- preceding the source CD-ROM filenames.

### Step 2: Extract article text and metadata
This step extracts contents (text) of each article and saves one *untokenized* .txt file per article in directory "data/articles/". The metadata for each article contained in XML attributes is saved separately as a CSV file in the "data/" directory. No metadata is saved in the .txt files themselves.

The naming scheme I used is "articleID_issue_author_title.txt", where articleID is a simple counter of articles that increments as they are processed. This was an arbitrary choice and can be changed easily, but beware of the small number of articles where issue, author, and title are not enough to create unique filenames.

### Step 3: Tokenize article text with MeCab
Finally, tokenize the article text in Step 2 output files, inserting whitespace between "words" as parsed by MeCab using the 近代文語UniDic. The resulting text is saved as a new set of article files in directory "data/tokenized/", with t- preceding filenames in the "articleID_issue_author_title.txt" format of Step 2.

## Final output
* "data/taiyo_metadata.csv" -- CSV containing all article metadata retained from original files' XML tags. Columns are:
  * articleid (4-digit counter for uniqueness)
  * issue (publication date as YYYYMM)
  * title
  * author
  * section ('欄名', such as 論説, 名家談叢, 海外事情)
  * style ('文体', spoken or written)
  * genre ('ジャンル', as [NDC codes](https://www.jla.or.jp/committees/bunrui/tabid/187/Default.aspx))
* "data/tokenized/*.txt" -- UTF-8 text files containing article contents, tokenized with whitespace between words using MeCab (no metadata saved inside files). One file per article in format "issue_author_title.txt"

*Note*: Missing or N/A author value is indicated in CSV and filenames with ＊. For example:
```
t-0001_190103_＊_〈扉〉.txt
t-0002_190103_＊_憲政の一大危機.txt
```
Missing section ＊＊ and genre ＊＊＊ values also appear in the CSV.

## Further resources
- [Taiyō Corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html)
- [UniDic download & documentation page](https://ccd.ninjal.ac.jp/unidic/en/download_all_en)
- [NINJAL 国立国語研究所 homepage](https://www.ninjal.ac.jp/)
- Aurora Tsai's guide to [installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798)
- [MeCab-Pythonで分かち書きと形態素解析](https://testpy.hatenablog.com/entry/2016/10/04/010000) by [Shoto](https://github.com/iShoto)
- [Japanese NLP posts](https://www.dampfkraft.com/nlp.html) by Paul O'Leary McCann at Dampfkraft


## Reuse
Copyright Molly Des Jardin

I wrote these scripts for my own, one-time personal use, and no longer maintain them. There are doubtless many improvements it could use (not least, command line arguments or a config file instead of hard-coding). Please feel free to reuse or enhance this basic code in your own projects.


*MIT License*

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
