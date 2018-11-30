from __future__ import unicode_literals
from isc_tokenizer import Tokenizer
from isc_tagger import Tagger
from isc_parser import Parser
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-in", "--input_file", help="Input File")
parser.add_argument("-out", "--output_file", help="Output File")

args = parser.parse_args()

# input_file = open(args.input_file)
# input_text = input_file.readline()
# dict_file_nel = open('../../Downloads/NER-LIST-UTF/NEL.txt.utf')
# tk_ner = Tokenizer(lang='hin')
# tagger = Tagger(lang='hin')

# seq = tk_ner.tokenize("छह")
# list_tagged = tagger.tag(seq)

# for word in list_tagged:
#     print(word)

#parser - WORKS(not required as  of now)
parser = Parser(lang='hin')
# text3 = "भारत शासन अधिनियम, 1935 में परिभाषित भारत में जन्मा था"
text3 = "19 जुलाई, 1948	के पश्चात् प्रव्रजन किया है, 12-6-2014"
text3 = text3.split()
tree = parser.parse(text3)
print('\n'.join(['\t'.join(node) for node in tree]))


# #tokenizer - WORKS
# tk1 = Tokenizer(lang='eng', smt=True)
# text1 = "the quick brown fox jumped over the watchful dog"
# list1 = tk1.tokenize(text1)

# print(list1[0]) #prints (the)
# #--------------------------------------------------------------

# #tagger - WORKS
# tk2 = Tokenizer(lang='hin')
# tagger = Tagger(lang='hin')
# sequence = tk2.tokenize("हम , भारत के लोग , भारत को एक संपूर्ण प्रभुत्व - संपन्न समाजवादी पंथनिरपेक्ष लोकतंत्रात्मक गणराज्य बनाने के लिए")
# list2 = tagger.tag(sequence)

# print(list2[0][1]) #prints (PRP)
# #--------------------------------------------------------------

# #parser - WORKS(not required as  of now)
# parser = Parser(lang='hin')
# text3 = "हम , भारत के लोग , भारत को एक संपूर्ण प्रभुत्व - संपन्न समाजवादी पंथनिरपेक्ष लोकतंत्रात्मक गणराज्य बनाने के लिए"
# text3 = text3.split()
# tree = parser.parse(text3)
# print('\n'.join(['\t'.join(node) for node in tree]))