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
# Step 1 of Taiyo Corpus Tools
#
# This script performs to tasks on a directory of .xml files:
# Convert Shift-JIS encoding to UTF-8, ignoring # errors. This assumes there can
# be issues with the input files that would cause the script to stop otherwise.
# The output files may be missing characters as as result.
#
# Replaces Japanese XML tag and attribute names with ASCII equivalent. Romaji is 
# used for Japanese-specific linguistic terms that can't be expressed simply in 
# English; for more common terms I chose an English translation.
#
# Not all tag/attribute names are converted here. Those not used in later steps 
# of the Taiyo Corpus Tools are ignored here and left as-is.
#
#
# Output is UTF-8, XML files written to directory 'data/articles/' with prefix 
# 'u-' added to the original filename. With the NINJAL Taiyo Corpus as source, 
# the output is one .xml file per magazine issue.

from pathlib import Path

inpath = Path.cwd().joinpath('data', 'taiyo_cd', 'XML')
if (not(inpath.is_dir())):
    print('input directory must exist relative to this script')
    raise SystemExit(1)
outpath = Path.cwd().joinpath('data', 'utf8')
if (not(outpath.exists())):
    outpath.mkdir()
infiles = inpath.glob('*.xml')

replacements = {
    'encoding="Shift_JIS"':'encoding="UTF-8"',
    '<記事':'<article',
    '題名=':'title=',
    '著者=':'author=',
    '欄名=':'section=',
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
    '<非入力対象':'<ne',
    '</非入力対象':'</ne'
    }

for filename in infiles:
    with open(filename, mode='r', encoding='Shift-JIS', errors='ignore') as f:
        lines = f.read()
    for key in replacements.keys():
        lines = lines.replace(key,replacements[key])

    with open(outpath.joinpath('u-' + filename.name), mode='w', 
    encoding='utf-8') as f:
        f.write(lines)
