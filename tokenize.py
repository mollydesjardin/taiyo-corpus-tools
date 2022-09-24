#!/usr/bin/env python3
# -*- coding: utf_8 -*-

"""
This assumes you have a directory of UTF-8 Japanese .txt files to batch
tokenize, and already installed/tested MeCab and your preferred dictionary.

Performs whitespace tokenization ONLY. Other MeCab parsing options return a
data structure with grammatical information about individual words. Wakati
simply returns text with whitespace inserted between tokens.

This script writes out that whitespace-tokenized text in a new file with a t-
prefix + input filename to the input directory.
"""


import MeCab, glob

m = MeCab.Tagger("-Owakati")

for filename in glob.iglob("data/articles/*.txt"):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        parsed = m.parse(text)
        output_filename = 'data/tokenized/t-{}'.format(filename[9:])
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(parsed)
