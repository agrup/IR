from compresor import *
from structure import *

voc_file = "voc_wiki.txt"
posting_file="posting_list_wiki.bin"
compersed_file_elias="posting_wiki_compress_elias.bin"

len_data=len(binary_pack([1],FORMAT_STRUCT))
FORMAT_STRUCT="{}B"
FORMAT_SIZE=3 

# def binary_pack(list,FORMAT_STRUCT): 
#     s_format=FORMAT_STRUCT.format(len(list))
#     return (struct.pack(s_format,*list)


vocavulary =read_voc(voc_file)

#posting=read_postin(postin_file,3,0,FORMAT_SIZE)
import math


# print(to_dgaps([10,11,12,15]))

# print=elias_gama([10,20,3,4])  




with open(compersed_file_elias,"wb") as file:
    for term ,(df,pt) in vocavulary.items():
        #print(term,df,pt)
        posting= read_postin(posting_file,df,pt,len_data)
        
        # for doc_id in posting:
        integer_bin=elias_gama(posting)  
        strc = struct.pack("B" * len(integer_bin), *integer_bin)
        file.write(strc)

with open("dgaps"+compersed_file_elias,"wb") as file:
    for term ,(df,pt) in vocavulary.items():

        posting= read_postin(posting_file,df,pt,len_data)
        integer_bin=elias_gama(to_dgaps(posting))    
        strc = struct.pack("B" * len(integer_bin), *integer_bin)

        file.write(strc)



