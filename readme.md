# Taiyō Corpus Tools
_last updated 12 March, 2023_

## Intro
Taiyō Corpus Tools is a set of short Python scripts that preprocesses Japanese-language text from [NINJAL's Taiyō 太陽 magazine corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html) for use with common analysis software. Each step produces usable output so the full series does not need to be run, depending on your needs:

* 1-convert_shiftjis_utf8.py -- convert NINJAL's Shift-JIS-encoded, XML files of monthly magazine issues to UTF-8 with ASCII XML tags/attributes

* 2-extract_metadata_text.py -- export article text content only to individual files; save article-level metadata from XML tags to single CSV

* 3-tokenize.py -- insert whitespace between words in article text using MeCab and save final output as individual, tokenized text files

### Requirements
* NINJAL Taiyō Corpus data files (see [Get the source data](#get-the-source-data) below)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [mecab-python3](https://pypi.org/project/mecab-python3/)
* MeCab, if not installed by mecab-python3 automatically
* [近代文語UniDic](https://clrd.ninjal.ac.jp/unidic/) (UniDic for Modern Literary Japanese, suggested)
* Configure MeCab to use non-default dictionary (suggested)

## Get started
### Set up your environment
Tokenization requires mecab-python3, which may install MeCab for you on some systems; otherwise, install MeCab itself first. If using a custom dictionary, either configure your system first, or specify the path to the dictionary files [in step 3 (tokenization)](#running-the-scripts). There are many guides to installing/configuring MeCab available online, so I don't provide (probably stale) instructions here. See [Further Resources](#further-resources) for suggestions.

Using 近代文語UniDic is optional, but should produce better word-splitting results than a 21st-century default because it most closely matches Taiyō's language.

#### MeCab and Dictionary Config Note
If you mostly use MeCab with a Python wrapper (ex. mecab-python3 or fugashi), it may install a MeCab binary for you (without separate steps needed). Using a Python environment (ex. conda) rather than directly installing to your system is also increasingly common. However, the resulting directories and files created are very different from those assumed in many MeCab configuration guides out there online.

The [tokenization step](#running-the-scripts) contains an alternate line of code for instantiating a MeCab.Tagger that I suggest using if this sounds like your setup. It ignores mecabrc (config file) and specifies the dictionary path, avoiding the need to find where these files may (not have been) installed. You can also be certain MeCab is using the intended dictionary.

### Directory structure
All three scripts assume the directory structure below, where they are in the root project folder. Each script saves its output as a new set of files without overwriting anything, and will first create its output directory in "data/" if needed.

"data/taiyo_cd/" contains the corpus CD-ROM data, _not included here_. Before running the scripts, _make sure the data/taiyo_cd/XML/ directory exists and includes the initial XML input files_, or that the path in the first script reflects where the data is on your system. This is the only expected input not created by a previous step.

```
Taiyo/
|-- 1-convert_shiftjis_utf8.py
|-- 2-extract_metadata_text.py
|-- 3-tokenize.py
`-- data/
    |-- taiyo_metadata.csv
    |-- articles/
    |   |-- 189501001_＊_〈扉〉.txt
    |   |-- 189501002_大橋新太郎_太陽の発刊.txt
    |   |-- 189501003_久米邦武_学界の大革新.txt
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
    |   |-- t-189501001_＊_〈扉〉.txt
    |   |-- t-189501002_大橋新太郎_太陽の発刊.txt
    |   |-- t-189501003_久米邦武_学界の大革新.txt
    |   |-- ...
    `-- utf8/
        |-- u-t189501.xml
        |-- u-t189502.xml
        |-- ...
        `-- u-t192514.xml
```

### Get the source data
This repo **does not contain** the data files that make up NINJAL's corpus, which are obtained from the [2005 CD-ROM edition](http://www.hakubunkan.co.jp/gengo/taiyoC.html). It may still be available for sale, but below are some other suggestions to get the text data for personal use.

The Taiyō Corpus is now part of the [Meiji/Taishō historical corpora](https://clrd.ninjal.ac.jp/chj/meiji_taisho.html) available on NINJAL's Chūnagon 中納言 corpus browser platform (free with registration). Contact NINJAL directly to learn what data might be available from them directly.

Some university libraries own the CD-ROM and lend it via Inter-Library Loan (see the [Worldcat entry](http://www.worldcat.org/oclc/191854098) for an example in North America). If you are affiliated with a university, you may be able to get access through your own library/ILL.

_A version of the Taiyō magazine archives is also available on the JapanKnowledge platform, which some universities license. It is **not compatible** with these scripts because it does not contain the same data._


## Background
### Why?
Short and simple as it looks now, when I started trying to work with NINJAL's Taiyō Corpus in 2015, I could find almost no documentation that really addressed the issues I ran into. I was still using Python 2.7 at the time, so dealing with UTF-8 or Shift-JIS encoding was also much more of a struggle.

I spent a long time searching online and reading Japanese or English blog posts that were mainly about something else, cobbling together a solution to my issues with various tidbits. (I got some invaluable tips on MeCab configuration directly from [Mark Ravina](https://liberalarts.utexas.edu/history/faculty/mr56267) as well.)

In 2023, some of the problems I encountered have solutions readily searchable online, or even better, aren't problems anymore because of developments in tools and software available. But Japanese-language documents are still not straightforward to work with (Taiyō Corpus or otherwise) so I am sharing my code in the hope it can be of help to someone else.

### About the data
NINJAL's Taiyō Corpus contains full-text articles from [Taiyō 太陽 magazine](https://ja.wikipedia.org/wiki/%E5%A4%AA%E9%99%BD_%28%E5%8D%9A%E6%96%87%E9%A4%A8%29) (published 1895-1928). The corpus includes thousands of articles from 1895, 1901, 1909, 1917, and 1925. You can find more info about this particular corpus on [NINJAL's website](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html).

The dataset consists of one XML file per magazine issue, with both text and metadata. The article text is hand-corrected and annotated with linguistic data, including at the word level, so the quality is much better than OCR on documents from this time/language. Metadata in the XML tags includes:
- publishing information for the magazine issues
- publishing information for each article (author, title, genre)
- linguistic attributes at the article or word level (style of speech, and glosses of errors or rare kanji that could not be entered at the time).

Article text is tokenized at the sentence level only with `<s>` tag, and I disregard that when tokenizing.

Note that while issue numbers in both filesnames and XML metadata resemble a year + month format, the numbers do not necessarily reflect their corresponding calendar months (Jan == 01, ..., Dec == 12). Refer to NINJAL's documentation and/or a reliable bibliographic source to check for actual publication dates per issue.

## Running the scripts
All three scripts operate assuming the [directory structure and files described above](#directory-structure). They should be run in the root project directory with no arguments.

### Step 1: Shift-JIS to Unicode and XML normalization
The Taiyō XML files contain many XML elements and attributes named in Japanese. While this is valid XML, it presents a problem for parsing libraries (as of this writing). This script replaces all non-ASCII tag and element names with romanized or English keyword equivalents. Output is saved as one UTF-8 .xml file per magazine issue, in directory "data/utf8/" with u- preceding the source CD-ROM filenames.

### Step 2: Extract article text and metadata
This step extracts contents (text) of each article and saves one *untokenized* .txt file per article in directory "data/articles/". The metadata for each article contained in XML attributes is saved separately as a CSV file in the "data/" directory. No metadata is saved in the .txt files themselves.

The naming scheme I chose is "articleid_author_title.txt", where articleid is the issue year/number (YYYYNN) plus a 3-digit counter (reset per issue) for uniqueness. If you prefer different naming, note that issue/author/title alone is **not unique enough** to prevent some identically-named files.

### Step 3: Tokenize article text with MeCab
Finally, tokenize the article text in Step 2 output files, inserting whitespace between "words" as parsed by MeCab using the 近代文語UniDic. (This is done after discarding the `<s>` tag in Step 2 so it does not take sentence boundaries into account.) The resulting text is saved as a new set of article files in directory "data/tokenized/", with t- preceding filenames in the "articleid_author_title.txt" format of Step 2.

If you already have MeCab installed and configured as you want, run the script as-is with the default Tagger instantiation (using only option "-Owakati"). If you have not done the configuration on your system already, un-comment the alternate line to point MeCab to the dictionary you want it to use. Fill in the path to reflect your system and remove or comment out the default (now unused) Tagger instantiation before running.

## Final output
* "data/taiyo_metadata.csv" -- CSV containing all article metadata retained from original files' XML tags. Columns are:
  * articleid (issue + 3-digit counter for uniqueness)
  * issue (YYYYNN format, where YYYY is year in Western calendar and NN is number)
  * title
  * author
  * section ('欄名', such as 論説, 名家談叢, 海外事情)
  * style ('文体', spoken or written)
  * genre ('ジャンル', as [NDC codes](https://www.jla.or.jp/committees/bunrui/tabid/187/Default.aspx))
* "data/tokenized/*.txt" -- One file per article in format "t-articleid_author_title.txt", UTF-8 encoding, article text only, tokenized using MeCab.

*Note*: Missing or N/A author value is indicated in CSV and filenames with ＊. For example:
```
t-189501001_＊_〈扉〉.txt
```
Missing section ＊＊ and genre ＊＊＊ values also appear in the CSV. This designation is from the original XML files.

## Further resources
- [Taiyō Corpus](https://ccd.ninjal.ac.jp/cmj/taiyou/index.html)
- [UniDic download & documentation page](https://ccd.ninjal.ac.jp/unidic/en/download_all_en)
- [NINJAL 国立国語研究所 homepage](https://www.ninjal.ac.jp/)
- [mecab-python3 source code & documentation](https://github.com/SamuraiT/mecab-python3) -- includes helpful troubleshooting tips
- Aurora Tsai's guide to [installing MeCab and MeCab Python Wrapper](https://rpubs.com/auroratsai/462798)
- [MeCab-Pythonで分かち書きと形態素解析](https://testpy.hatenablog.com/entry/2016/10/04/010000) by [Shoto](https://github.com/iShoto)
- [Japanese NLP posts](https://www.dampfkraft.com/nlp.html) by Paul O'Leary McCann at Dampfkraft


## Reuse
Copyright Molly Des Jardin

I wrote these scripts for my own, one-time personal use, and no longer maintain them. Please feel free to reuse or improve this basic code in your own projects.


*MIT License*

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
