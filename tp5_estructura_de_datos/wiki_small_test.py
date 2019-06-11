
from structure import *
from modulos.tokenizer import tokenizar
from TAAT import *
from query_parse import *
import datetime
import time


FORMAT_STRUCT="{}I"
FORMAT_SIZE=4
postin_file="posting_list_wiki.bin"
voc_file="voc_wiki.txt"

query_file="/home/agu/Unlu/IR/colecciones/wiki/queries_2y3t.txt"

dirname="/home/agu/Unlu/IR/colecciones/wiki/en/"

# vocs,posting = (indexer(dirname))
# save_posting(vocs,posting,postin_file,FORMAT_STRUCT)
# len_data=len(binary_pack([1],FORMAT_STRUCT))
# size = int(os.path.getsize(postin_file)/len_data)   
# save_voc(vocs,voc_file)


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

posting_dic={}
with open(postin_file,"rb") as index:
    size_obj_index=sys.getsizeof(index)
    tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
    tuple_array = np.array(tuple_index)
    terms=[]
    for term, (value,pt) in vocs_id.items():
        index.seek(int(pt))
        docus=index.read(int(value)*len_data)
        postin=struct.unpack(FORMAT_STRUCT.format(value),docus)
        posting_dic[term]=postin
# print(tuple_array)

three_terms_querys=[]
two_terms_querys=[]

with open(query_file,"r") as querys_list:
    lines = querys_list.readlines()
    for line in lines:
        if len(line.split())==2:
            two_terms_querys.append(line.split())
        elif len(line.split())==3:
            three_terms_querys.append(line.split())

# print(tree_terms_querys)



print("iniciando querys con postings en memoria")
print(datetime.datetime.now(),"Inicio en memoria")
start = time.time()

for query_array in two_terms_querys:
    query=str(query_array[0])+" AND "+str(query_array[1])    

    # print(query)
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)
    # Segunda consulta
    query=str(query_array[0])+" OR "+str(query_array[1])
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)
    # Tercera query
    query=str(query_array[0])+" AND NOT "+str(query_array[1])
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)

print(datetime.datetime.now(),"Fin de querys en memoria con dos terminos")

for query_array in three_terms_querys:
    query = str(query_array[0])+" AND "+str(query_array[1])+" AND "+str(query_array[2])
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)

    query = str(query_array[0])+" AND NOT"+str(query_array[2])+" OR "+str(query_array[1])+" AND NOT "+str(query_array[2])
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)

    query = str(query_array[0])+" AND "+str(query_array[1])+" OR "+str(query_array[2])
    query =token_query(query)
    find_memory(query,vocs_id,FORMAT_STRUCT,posting_dic)

done = time.time()
print(datetime.datetime.now(),"Fin de querys en memoria con tres terminos")
print("Resultado:",done - start)

print(datetime.datetime.now(),"Inicio en Archivo")
start = time.time()

for query_array in two_terms_querys:
    query=str(query_array[0])+" AND "+str(query_array[1])    
    # print(query)
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)
    # Segunda consulta
    query=str(query_array[0])+" OR "+str(query_array[1])
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)
    # Tercera query
    query=str(query_array[0])+" AND NOT "+str(query_array[1])
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)



print(datetime.datetime.now(),"Fin de querys en disco con dos terminos")

for query_array in three_terms_querys:
    query = str(query_array[0])+" AND "+str(query_array[1])+" AND "+str(query_array[2])
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)

    query = str(query_array[0])+" AND NOT"+str(query_array[2])+" OR "+str(query_array[1])+" AND NOT "+str(query_array[2])
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)

    query = str(query_array[0])+" AND "+str(query_array[1])+" OR "+str(query_array[2])
    query =token_query(query)
    find(query,vocs_id,FORMAT_STRUCT,postin_file)

done = time.time()
print(datetime.datetime.now(),"Fin de querys en disco con tres terminos")

print("Resultado:",done - start)








