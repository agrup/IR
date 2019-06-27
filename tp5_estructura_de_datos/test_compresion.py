from compresor import * 
from structure import *
import time 
import math
import datetime

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



# print(to_dgaps([10,11,12,15]))

# print=elias_gama([10,20,3,4])  


print("ELIAS Gamma")
start = time.time()


with open(compersed_file_elias,"wb") as file:
    for term ,(df,pt) in vocavulary.items():
        #print(term,df,pt)
        posting= read_postin(posting_file,df,pt,len_data)
        
        # for doc_id in posting:
        integer_bin=elias_gamma(posting)
        size_posting = len(integer_bin)
        # print(integer_bin,posting)
        # size_strc = struct.pack("I",size_posting)
        # file.write(size_strc)   
        strc = struct.pack("B" * len(integer_bin), *integer_bin)
        # print(size_posting,"size posting save",posting,"posting",integer_bin,"integer bin",len(strc),strc)

        file.write(strc)

done = time.time()
print(datetime.datetime.now(),"Compresion con lista de docsid")
print("Resultado:",done - start)

start = time.time()


with open("dgaps"+compersed_file_elias,"wb") as file:
    for term ,(df,pt) in vocavulary.items():

        posting= read_postin(posting_file,df,pt,len_data)
        integer_bin=elias_gamma(to_dgaps(posting))   
        size_posting = len(integer_bin)
        # size_strc = struct.pack("I",size_posting)
        # file.write(size_strc) 
        strc = struct.pack("B" * len(integer_bin), *integer_bin)

        file.write(strc)


done = time.time()
print(datetime.datetime.now(),"Compresion con lista de dgaps")
print("Resultado:",done - start)

start = time.time()

with open(compersed_file_elias,"rb") as file:
    len_byte=len(binary_pack([1],'{}I'))

    int_size_posting=file.read()


    bin_posting = struct.unpack("B"*len(int_size_posting),int_size_posting)
    # print(bin_posting)
    # print(undecode_elias_gama(bin_posting))
    print("************************")
done = time.time()
print(datetime.datetime.now(),"descompresion docs id")
print("Resultado:",done - start)


start = time.time()

with open("dgaps"+compersed_file_elias,"rb") as file:
    len_byte=len(binary_pack([1],'{}I'))

    int_size_posting=file.read()


    bin_posting = struct.unpack("B"*len(int_size_posting),int_size_posting)
    # print(bin_posting)
    # print(undecode_elias_gama(bin_posting))
    print("************************")

done = time.time()
print(datetime.datetime.now(),"descompresion docs con d gaps")
print("Resultado:",done - start)