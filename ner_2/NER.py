from __future__ import unicode_literals
from isc_tokenizer import Tokenizer
from isc_tagger import Tagger
from isc_parser import Parser
import argparse
import matplotlib.pyplot as plt

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
output_file = open(args.output_file,"w")
dict_file_nel = open('../../../Downloads/NER-LIST-UTF/NEL.txt.utf')
tk_ner = Tokenizer(lang='hin')
tagger = Tagger(lang='hin')

seq = tk_ner.tokenize(input_text)
# print(seq[0])
# list_ner = tagger.tag(seq)

dict_read_nel = dict_file_nel.read()
dict_word_nel = tk_ner.tokenize(dict_read_nel)
count=-1

tag_dict = {}

dict_nem = open('./NER-LIST-UTF/NEM.txt.utf')
text = dict_nem.read()
seq_dict_nem =  tk_ner.tokenize(text)
dict_nem1 = open('./NER-LIST-UTF/test.txt.utf')
text1 = dict_nem1.read()
seq_dict_nem1 = tk_ner.tokenize(text1)
dict_neo = open('./NER-LIST-UTF/NEO.txt.utf')
text_neo = dict_neo.read()
seq_dict_neo = tk_ner.tokenize(text_neo)
for word in seq:
    count+=1 
    flag=0
    # print(dict_word)
    tokenised_word = tk_ner.tokenize(word)
    tag = tagger.tag(tokenised_word)

    #B-NEL(countries, states, etc.)-------------------------------------------
    if(tag[0][1] == "NNP"):
        for i in dict_word_nel:
            if(word == i and not count in tag_dict):
                tag_dict[count]='B-NEL'
                break
            else:
                continue
    
    #B-Section(Section 377 etc.)----------------------------------------------
    elif word == "धारा":
        tokenised_word2 = tk_ner.tokenize(seq[count+1])
        tag_next = tagger.tag(tokenised_word2)
        if(tag_next[0][1] == "QC"):
            tag_dict[count]='B-Section'
            tag_dict[count+1]='I-Section'

    #B-Article---------------------------------------------------
    elif word == "अनुच्छेद":
        tokenised_word3 = tk_ner.tokenize(seq[count+1])
        tag_next = tagger.tag(tokenised_word3)
        if(tag_next[0][1] == "QC"):
            tag_dict[count]='B-Article'
            tag_dict[count+1]='I-Article'

    #B-Schedule-----------------------------------------------------
    elif word == "अनुसूची":
        tokenised_word4 = tk_ner.tokenize(seq[count-1])
        tag_next = tagger.tag(tokenised_word4)
        if(tag_next[0][1] == "QO"):
            tag_dict[count-1]='B-Schedule'
            tag_dict[count]='I-Schedule'

    #B-Case(A and others v/s B and others)-----------------------------
    elif word == "बनाम":
        up_iterator = count
        down_iterator = count
        while True:
            tokenised_word5 = tk_ner.tokenize(seq[up_iterator])
            if flag == 0 and tagger.tag(tokenised_word5)[0][1]=='NNP':
                flag=1
            tokenised_word6 = tk_ner.tokenize(seq[up_iterator])
            if flag ==1 and tagger.tag( tokenised_word6)[0][1]!='NNP':
                tag_dict[up_iterator]='B-Case'
                break
            tag_dict[up_iterator]='I-Case'
            up_iterator-=1
        flag = 0

        while True:
            evaluate = (seq[down_iterator]=='एस' and seq[down_iterator+1]=='.' and seq[down_iterator+2]=='सी' and seq[down_iterator+3]=='.' and seq[down_iterator+4]=='आर' and seq[down_iterator+5]=='.')
            if(seq[down_iterator]=="एससीसी" or evaluate == True):
                flag=1
            tokenised_word7 = tk_ner.tokenize(seq[down_iterator])
            if flag==1 and tagger.tag(tokenised_word7)[0][1] == 'QC':
                break
            down_iterator+=1
            tag_dict[down_iterator]='I-Case'

    #B-NEM------------------------------------------------------------------
    elif word in seq_dict_nem:
        tokenised_word8 = tk_ner.tokenize(seq[count-1])
        tag_prev = tagger.tag(tokenised_word8)
        if(tag_prev[0][1]=="QC"):
            tag_dict[count] = "I-NEM"
            tag_dict[count-1] = "B-NEM"

    #B-NETI------------------------------------------------------------------
    elif tag[0][1] == 'QC':
        tokenised_word9 = tk_ner.tokenize(seq[count+2])
        tag_month = tagger.tag(tokenised_word9)
        tokenised_word10 = tk_ner.tokenize(seq[count+4])
        tag_year = tagger.tag(tokenised_word)
        if seq[count+1]=='-' and tag_month[0][1]=='QC' and seq[count+3]=='-'and tag_year[0][1]=='QC':
            tag_dict[count]='B-NETI'
            tag_dict[count+1]='I-NETI'
            tag_dict[count+2]='I-NETI'
            tag_dict[count+3]='I-NETI'
            tag_dict[count+4]='I-NETI'
        elif seq[count+1] in seq_dict_nem1:
            tokenised_word11 = tk_ner.tokenize(seq[count+3])
            tag_year1 = tagger.tag(tokenised_word11)
            if seq[count+2]==',' and tag_year1[0][1]=='QC':
                tag_dict[count]='B-NETI'
                tag_dict[count+1]='I-NETI'
                tag_dict[count+2]='I-NETI'
                tag_dict[count+3]='I-NETI'

    #B-NEO-------------------------------------------------------------------
    elif word in seq_dict_neo:
        index = seq_dict_neo.index(word)
        first = index
        if seq_dict_neo[index-1]=='':
            while True:
                evaluate = seq[count]==seq_dict_neo[index]
                if evaluate and seq_dict_neo[index+1]=="":
                    break
                count+=1
                index+=1
                tag_dict[count]='I-NEO'
            tag_dict[first]='B-NEO'

            # tag_dict[count]='B-NEO'
            # if seq[count+1] == seq_dict_neo[index+1]:
            #     tag_dict[count]='B-NEO'
            #     tag_dict[count+1]='I-NEO'

    else:
        if not count in tag_dict:
            tag_dict[count]='O'

# print(tag_dict)

for key,value in tag_dict.items():
    output_file.write("{}\t\t{}\n".format(seq[key], value))
    # print("{}\t\t{}\n".format(seq[key], value))

NEL_Counter = 0
Section_Counter = 0
Article_Counter = 0
Schedule_Counter = 0
Case_Counter = 0
NEM_Counter = 0

for key,value in tag_dict.items():
    if(value == "B-NEL"):
        NEL_Counter+=1
    elif(value == "B-Section"):
        Section_Counter+=1
    elif(value == "B-Article"):
        Article_Counter+=1
    elif(value == "B-Schedule"):
        Schedule_Counter+=1
    elif(value == "B-Case"):
        Case_Counter+=1
    elif(value == "B-NEM"):
        NEM_Counter+=1

#change these 2 variables to suit your needs
NEL = NEL_Counter
Section = Section_Counter
Article = Article_Counter
Schedule = Schedule_Counter
Case = Case_Counter
NEM = NEM_Counter

plt.rcParams.update({'font.size': 22}) #adjust font size; not really needed

plt.pie([NEL, Section, Article, Schedule, Case, NEM],
        colors=["green","red", "blue","pink", "yellow", "purple"],
        labels=["NEL", "Section", "Article", "Schedule", "Case", "NEM"],
        autopct='%1.1f%%', 
        startangle=90)

plt.axis('equal') #ensure pie is round
plt.show()



