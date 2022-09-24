#!/usr/bin/env python3
# -*- coding: utf_8 -*-

"""
Converts a directory of .xml files (substitute path and extension as needed)
from Shift-JIS encoding to UTF-8, ignoring errors.

This assumes there may be occasional unexpected characters in the input
files, and you would prefer to skip them, read in and convert what you can.

While the XML is read in as a string (not parsed) the script also replaces
kanji-based XML tags/attributes with ASCII equivalent to make working with
Beautiful Soup in future steps easier. Romaji is used for Japanese-specific
linguistic terms that can't be expressed simply in English; otherwise they are
translated simply.

Attributes that go unused in further processing are *not*
romanized or translated -- this is only to avoid problems with libraries that
expect a limited character set in tag/attribute names.

For those working with the full CD-ROM files and are interested in
textual metadata like the portions of articles marked off as quotes, there are
additional attribtues within those tags that you may be interested in. The
text within articles is also generally marked up with linguistic and printing
specific tags that are ignored here.

This is an example of a quote tag marking the text enclosed as being
commentary by the article author:
<引用 種別="記事説明" 話者="記者">
...
</引用>

XML files are written out as UTF-8 with romaji-ized tags and u- prefix filenames
to the directory of the script.

"""


replacements = {
    'encoding="Shift_JIS"':'encoding="UTF-8"',
    '<記事':'<article',
    '題名=':'title=',
    '著者=':'author=',
    '欄名=':'column=',
    '文体=':'style=',
    'ジャンル=':'genre=',
    '</記事':'</article',
    '<注':'<note',
    '</注':'</note',
    '<合字':'<ligature',
    '</合字':'</ligature',
    '<引用':'<quote',
    '</引用':'</quote',
    '<外字':'<gaiji',
    '</外字':'</gaiji',
    '<敬意欠字':'<ketsuji',
    '</敬意欠字':'</ketsuji',
    '<踊字':'<odoriji',
    '</踊字':'</odoriji',
    '<非入力対象':'<unused',
    '</非入力対象':'</unused'
    }


import glob

for filename in glob.iglob('data/taiyo_cd/XML/*.xml'):
    with open(filename, mode='r', encoding='Shift-JIS', errors='ignore') as f:
        lines = f.read()
    for key in replacements.keys():
        lines = lines.replace(key,replacements[key])

    with open('data/utf8/u-' + filename[-11:], mode='w', encoding='utf-8') as f:
        f.write(lines)
