from __future__ import unicode_literals
from isc_tokenizer import Tokenizer
from isc_tagger import Tagger
from isc_parser import Parser
import argparse

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
# #--------------------------------------------------------------
#--------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("-in", "--input_file", help="Input File")
parser.add_argument("-out", "--output_file", help="Output File")

args = parser.parse_args()

# print( "input {} output {}".format(args.input_file,args.output_file))

input_file = open(args.input_file)
input_text = input_file.read()
dict_file_nel = open('../../../Downloads/NER-LIST-UTF/NEL.txt.utf')
tk_ner = Tokenizer(lang='hin')
tagger = Tagger(lang='hin')

seq = tk_ner.tokenize(input_text)
# print(seq[0])
# list_ner = tagger.tag(seq)

dict_read_nel = dict_file_nel.read()
dict_word_nel = tk_ner.tokenize(dict_read_nel)
for word in seq: 
    # print(dict_word)
    for i in dict_word_nel: 
        # print("word = {}, dict_word = {}".format(word, i))
        if(word == i):
            tokenised_word = tk_ner.tokenize(word)
            tag = tagger.tag(tokenised_word)
            if(tag[0][1] == "NNP"):
                print("word={}  dict={} tag={}".format(word, i, tag[0][1]))
                break
        else:
            continue

# print(list_ner)
