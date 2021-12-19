# -*- coding: utf-8 -*-

"""
This assumes you have a directory of UTF-8 Japanese .txt files to batch
tokenize, and already installed/tested MeCab and your preferred dictionary.

Performs whitespace tokenization ONLY. Other MeCab parsing options return a
data structure with grammatical information about individual words. Wakati
simply returns text with whitespace inserted between tokens.

This script writes out that whitespace-tokenized text in a new file with a p_
prefix + input filename to the input directory.
"""


import MeCab, glob

m = MeCab.Tagger("-Owakati")

for input_filename in glob.iglob("*.txt"):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        parsed = m.parse (text)
        output_filename = 'p_{}'.format(input_filename)
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(parsed)

