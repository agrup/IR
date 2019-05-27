import struct
from os import listdir
import os
from modulos.tokenizer import tokenizar
import math
import itertools
import numpy as np
import sys

#dirname = "/home/agu/Unlu/IR/tp5_estructura_de_datos/data"
dirname="/home/agu/Unlu/IR/colecciones/RI-tknz-data"

FORMAT_STRUCT="{}I"
FORMAT_SIZE=4
#size_dirname=0

def binary_pack(list):
    s_format=FORMAT_STRUCT.format(len(list))
    return (struct.pack(s_format,*list))
    
def binary_unpack(file,s_format):
    content = file.read()
    
    unpackage_data = struct.unpack(s_format,content)
    return unpackage_data

def calc_idf(corpus_count,doc_freq):
    if(doc_freq !=0):
        return math.log(corpus_count/doc_freq,2)
    return 0

def indexer(dirname):
        files = listdir(dirname)
        vocabulary={}
        document_vector={}
        id_voc=0
        #vocavulary_result=[]
        #docs_count=len(files)
        posting={}
        doc_id=0
        pt=0
        size_dirname=0
        size_disk=0
        for file in files:
            size_disk+=os.path.getsize(dirname+'/'+file)
            with open(dirname+'/'+file,'r',errors = 'ignore') as file_aux:
                lines = file_aux.readlines()
                size_dirname+=sys.getsizeof(file_aux)

            docu_voc=[]
            tokens=tokenizar(lines)
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token]=(id_voc,1)
                    docu_voc.append(id_voc)
                    posting[token]=[doc_id]
                    id_voc =id_voc+1
                else:
                    id,doc_freq = vocabulary[token]
                    if id not in docu_voc:
                        doc_freq = doc_freq+1
                        docu_voc.append(id)
                        posting[token].append(doc_id)
                    vocabulary[token]=(id,doc_freq)
                    pt+=doc_freq
            document_vector[file]=docu_voc
            
            doc_id+=1
        voc_id=[]
        #for termn in vocabulary.items():
        pt=0
        for term in sorted(vocabulary.keys()):
            df=vocabulary[term]
            voc_id.append((term,df[1],pt))
            pt+=df[1]*4
        #print(size_dirname)
        return (voc_id,posting,size_dirname,size_disk)


vocs,posting,size_dirname,size_disk = (indexer(dirname))
#print(vocs)
#print(int(os.path.getsize("index.bin")/FORMAT_SIZE))
with open("index.bin","wb") as index:
    for term, value,pt in vocs:
        index.write(binary_pack(posting[term]))



#TODO tengo que agregar los punteros en el vocabulario y luego poder recuperar los posting
len_data=len(binary_pack([1]))
#print(len_data)
size = int(os.path.getsize("index.bin")/len_data)
#print(os.path.getsize(dirname)-os.path.getsize("index.bin")-sys.getsizeof(vocs))
#size_obj_index=0
with open("voc.txt","w") as voc:
    for term, value,pt in vocs:
        voc.write(str(term)+" "+str(value)+" "+str(pt)+"\n")
#size_obj_index=os.path.getsize("voc.txt")

with open("index.bin","rb") as index:
    size_obj_index=sys.getsizeof(index)
    tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
    tuple_array = np.array(tuple_index)

    for term, value,pt in vocs:
        index.seek(pt)
        docus=index.read(value*len_data)
        postin=struct.unpack(FORMAT_STRUCT.format(value),docus)
        #print(term,np.array(postin))

print(os.path.getsize(dirname))
print("directori size",size_dirname,size_disk)
print("directori posting",size_obj_index,os.path.getsize("index.bin"))
print("directori index",sys.getsizeof(vocs),os.path.getsize("voc.txt"))
print("result",os.path.getsize("index.bin")+os.path.getsize("voc.txt")-size_disk)
print("result",size_obj_index+sys.getsizeof(vocs)-size_dirname)
#print(vocs)

    

