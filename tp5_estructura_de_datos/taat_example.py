from structure import * 
# from structure import
from TAAT import *
from query_parse import *
from modulos.tokenizer import tokenizar

FORMAT_STRUCT="{}I"
FORMAT_SIZE=4
postin_file="posting_list.bin"
voc_file="voc.txt"

len_data=len(binary_pack([1],FORMAT_STRUCT))
size = int(os.path.getsize(postin_file)/len_data)   

vocs=[]
vocs_id={}
with open(voc_file) as vocabulary:
    lines =vocabulary.readlines()
    for line in lines:
        term=line.split()
        vocs.append(term)
        vocs_id[term[1]]=(term[2],term[3])

query = "aa OR zool "

# tokens = tokenizar(query.split())

# print("tt",query)
query =token_query(query)
# print(query2,"3333333")
# print(str(query))

find(query,vocs_id,FORMAT_STRUCT)
