from __future__ import unicode_literals
from isc_tokenizer import Tokenizer
from isc_tagger import Tagger
from isc_parser import Parser
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-in", "--input_file", help="Input File")
parser.add_argument("-out", "--output_file", help="Output File")

args = parser.parse_args()

input_file = open(args.input_file)
input_text = input_file.readline()
# dict_file_nel = open('../../Downloads/NER-LIST-UTF/NEL.txt.utf')
tk_ner = Tokenizer(lang='hin')
tagger = Tagger(lang='hin')

seq = tk_ner.tokenize(input_text)
list_tagged = tagger.tag(seq)

for word in list_tagged:
    print(word)