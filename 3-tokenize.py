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
# Step 3 of Taiyo Corpus Tools
#
# Uses MeCab with 'wakati' (simple word-splitting) option to tokenize every file
# in source directory 'data/articles/*.txt', assuming they contain only contents
# to tokenize (no metadata) and are UTF-8 encoding.
#
# Tokenized text is output in separate files with 't-' prefix in directory 
# 'data/tokenized/'


import MeCab, glob

tagger = MeCab.Tagger("-Owakati")

for filename in glob.iglob("data/articles/*.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        parsed = tagger.parse(text)
        output_filename = 'data/tokenized/t-{}'.format(filename.split('/')[-1])
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(parsed)
