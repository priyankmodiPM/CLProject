from __future__ import unicode_literals
from isc_tokenizer import Tokenizer
from isc_tagger import Tagger
from isc_parser import Parser
import argparse
import itertools
import matplotlib.pyplot as plt
from time import sleep



# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()





def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

#--------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("-in", "--input_file", help="Input File")
parser.add_argument("-out", "--output_file", help="Output File")

args = parser.parse_args()

# print( "input {} output {}".format(args.input_file,args.output_file))

input_file = open(args.input_file)
input_text = input_file.read()
output_file = open(args.output_file,"w")
dict_file_nel = open('./NER-LIST-UTF/NEL.txt.utf')
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
dict_ned = open('./NER-LIST-UTF/NED.txt.utf')
text_ned = dict_ned.read()
seq_dict_ned = tk_ner.tokenize(text_ned)
dict_nem1 = open('./NER-LIST-UTF/test.txt.utf')
text1 = dict_nem1.read()
seq_dict_nem1 = tk_ner.tokenize(text1)
dict_neo = open('./NER-LIST-UTF/NEO.txt.utf')
text_neo = dict_neo.read()
seq_dict_neo = tk_ner.tokenize(text_neo)
split_neo_list = [list(y) for x,y in itertools.groupby(seq_dict_neo, lambda z: z == ',') if not x]


i=0
l = len(seq)
for word in seq:
    count+=1 
    flag = 0
    flag2 = 0
    flag3 = 0
    # print(dict_word)
    tokenised_word = tk_ner.tokenize(word)
    tag = tagger.tag(tokenised_word)
    neti_evaluator1 = (len(seq)-count-1) >= 4
    neti_evaluator2 = (len(seq)-count-1) >= 3
    if neti_evaluator1:
        tokenised_word9 = tk_ner.tokenize(seq[count+2])
        tag_month = tagger.tag(tokenised_word9)
        tokenised_word10 = tk_ner.tokenize(seq[count+4])
        tag_year = tagger.tag(tokenised_word10)
    
    if neti_evaluator1 or neti_evaluator2:
        tokenised_word11 = tk_ner.tokenize(seq[count+3])
        tag_year1 = tagger.tag(tokenised_word11)
    
    #B-Section(Section 377 etc.)----------------------------------------------
    if word == "धारा":
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
        if(tag_next[0][1] == "QO" or seq[count-1]=='नवीं'):
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

    #B-NED-----------------------------------------------------------------
    elif word in seq_dict_ned and word != ',' and word!='-':
        tag_dict[count] = "B-NED"
    #B-NEM------------------------------------------------------------------
    elif word in seq_dict_nem:
        tokenised_word8 = tk_ner.tokenize(seq[count-1])
        tag_prev = tagger.tag(tokenised_word8)
        if(tag_prev[0][1]=="QC"):
            tag_dict[count] = "I-NEM"
            tag_dict[count-1] = "B-NEM"

    #B-ACT-------------------------------------------------------------------
    elif word == "संविधान" and seq[count+1]=='(':
        down = count
        while True:
            if is_number(seq[down])==True:
                flag2=1
            if flag2==1:
                break
            # print(flag2)
            down+=1            
            tag_dict[down] = "I-Act"
        tag_dict[count] = "B-Act"

    elif word == "भारत" and seq[count+1]=="शासन" and seq[count+2]=="अधिनियम":
        down2 = count+2
        while True:
            if is_number(seq[down2])==True:
                flag3=1
            if flag3==1:
                break
            down2+=1
            tag_dict[down2] = "I-Act"
        tag_dict[count]="B-Act"
        tag_dict[count+1]="I-Act"
        tag_dict[count+2]="I-Act"

    elif word == "अधिनियम" and seq[count-1]==')':
        up_iterator2 = count
        down_iterator2 = count
        while True:
            tokenised_word11 = tk_ner.tokenize(seq[up_iterator2])
            if flag == 0 and (tagger.tag(tokenised_word11)[0][1]=='NNP' or seq[up_iterator2]=='संविधान'):
                flag=1
            tokenised_word12 = tk_ner.tokenize(seq[up_iterator2])
            if flag ==1 and tagger.tag( tokenised_word12)[0][1]!='NNP':
                tag_dict[up_iterator2]='B-Act'
                break
            tag_dict[up_iterator2]='I-Act'
            up_iterator2-=1
        flag = 0

        while True:
            if(is_number(seq[down_iterator2])==True):
                flag=1
            if flag==1:
                break
            down_iterator2+=1
            tag_dict[down_iterator2]='I-Act'
    
    #B-NETI------------------------------------------------------------------
    elif neti_evaluator1:
        if tag[0][1] == 'QC' and seq[count+1]=='-' and tag_month[0][1]=='QC' and seq[count+3]=='-'and tag_year[0][1] in ['NNP','QC'] :
            tag_dict[count]='B-NETI'
            tag_dict[count+1]='I-NETI'
            tag_dict[count+2]='I-NETI'
            tag_dict[count+3]='I-NETI'
            tag_dict[count+4]='I-NETI'
        elif tag[0][1] == 'QC' and seq[count+1] in seq_dict_nem1 and seq[count+2]==',' and tag_year1[0][1] in ['NNP','QC'] :
            tag_dict[count]='B-NETI'
            tag_dict[count+1]='I-NETI'
            tag_dict[count+2]='I-NETI'
            tag_dict[count+3]='I-NETI'
    
    #B-NEO-------------------------------------------------------------------
        for each_list in split_neo_list:
            iterthrough = 0
            local_flag = 0
            if (len(seq) - count -1) >= len(each_list):
                for each_word in each_list:
                    if seq[count+iterthrough] == each_word:
                        local_flag += 1
                        iterthrough += 1
                    else:
                        break
                if local_flag == len(each_list):
                    tag_dict[count] = 'B-NEO'
                    local_count = 1
                    while local_count < local_flag:
                        tag_dict[count+local_count]='I-NEO'
                        local_count += 1
    
    #B-NEL(countries, states, etc.)-------------------------------------------
    if(tag[0][1] == "NNP" and word in dict_word_nel and not count in tag_dict):
        tag_dict[count] = 'B-NEL'
    

    if not count in tag_dict:
        tag_dict[count]='O'

    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    i+=1

# print(tag_dict)

for key,value in tag_dict.items():
    output_file.write("{}\t\t{}\n".format(seq[key], value))


NEL_Counter = 0
Section_Counter = 0
Article_Counter = 0
Schedule_Counter = 0
Case_Counter = 0
NEM_Counter = 0
Act_Counter = 0
NETI_Counter = 0
NEO_Counter = 0
NED_Counter = 0

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
    elif(value == "B-Act"):
        Act_Counter +=1
    elif(value == "B-NETI"):
        NETI_Counter += 1
    elif(value == "B-NEO"):
        NEO_Counter += 1
    elif(value == "B-NED"):
        NED_Counter += 1
        
    

#change these 2 variables to suit your needs
NEL = NEL_Counter
Section = Section_Counter
Article = Article_Counter
Schedule = Schedule_Counter
Case = Case_Counter
NEM = NEM_Counter
Act = Act_Counter
NETI = NETI_Counter
NEO = NEO_Counter
NED = NED_Counter

plt.rcParams.update({'font.size': 15}) #adjust font size; not really needed

plt.pie([NEL, Section, Article, Schedule, Case, NEM, Act, NETI, NEO, NED],
        colors=["green", "red", "blue", "pink", "yellow", "purple", "orange", "cyan", "white", "brown"],
        labels=["NEL", "Section", "Article", "Schedule", "Case", "NEM", "Act", "NETI", "NEO", "NED"],
        autopct='%1.1f%%', 
        startangle=90)

plt.axis('equal') #ensure pie is round
plt.show()



