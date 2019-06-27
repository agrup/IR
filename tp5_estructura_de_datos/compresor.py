from structure import *
from modulos.tokenizer import tokenizar
from TAAT import *
from query_parse import *
import math
import struct


from numpy import * 

FORMAT_STRUCT="{}b"
# FORMAT_SIZE=4 
postin_file="data.bin"
voc_file="data.txt"
 

def elias_gamma(list):

    for integer in list:
        elias = ""
        log2int_faster = integer.bit_length()
        integer_string=bin(integer)[2:].zfill(log2int_faster)
        elias= '0'*log2int_faster+integer_string
    bytes_to_write = []
    for i in range(0, len(elias), 8):
        substring = elias[i:i+8]
        byte = int(substring, 2)
        bytes_to_write.append(byte)
    return bytes_to_write

def undecode_elias_gama(bin_list):
    posting=""
    for byte in bin_list:
        posting += bin(byte)[2:]
    ceros=0
    flag =True
    posting_result=[]
    int_bin=""
    for i in range(0,len(posting)):
        # print(posting[i])
        if (posting[i] =='0'):
            ceros+=1
            i+=1
        elif( posting[i]=='1' and ceros != -1):
            
            # ceros -=1
            # print("casa",posting[i:i+ceros+1],ceros+1,i)
            int_bin=posting[i:i+ceros+1]
            ceros=0
            i+=ceros+1
                # print(int(int_bin,2))
            # print(int_bin)
            posting_result.append(int(int_bin,2))
            int_bin=[]
    return(posting_result)





def to_dgaps(postings):
    new_posting =[]
    init = postings[0]
    ant = init
    for posting in postings:
        if posting == init:
            new_posting.append(init)
        else:
            new_posting.append(posting-ant)
            ant = posting
    return new_posting

# def variable_lenght(postings):
