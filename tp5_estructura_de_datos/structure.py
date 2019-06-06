import struct
from os import listdir
import os
from modulos.tokenizer import tokenizar
import math
import itertools
import numpy as np
import sys
import matplotlib.pyplot as plt
import operator

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
        posting={}
        doc_id=0
        pt=0
        size_dirname=0
        size_disk=0
        for file in files:
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
        pt=0
        for term in sorted(vocabulary.keys()):
            df=vocabulary[term]
            voc_id.append((term,df[1],pt))
            pt+=df[1]*4
        #print(size_dirname)
        return (voc_id,posting,size_dirname,size_disk)

def plot_bar(values,label):
    index= np.arange(len(label))
    plt.bar(index,values)
    plt.xticks(index, label, fontsize=10, rotation=30)
    plt.show()

vocs,posting,size_dirname,size_disk = (indexer(dirname))


with open("index.bin","wb") as index:
    for term, value,pt in vocs:
        index.write(binary_pack(posting[term]))



len_data=len(binary_pack([1]))
size = int(os.path.getsize("index.bin")/len_data)
with open("voc.txt","w") as voc:
    for term, value,pt in vocs:
        voc.write(str(term)+" "+str(value)+" "+str(pt)+"\n")

with open("index.bin","rb") as index:
    size_obj_index=sys.getsizeof(index)
    tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
    tuple_array = np.array(tuple_index)
    terms=[]
    for term, value,pt in vocs:
        index.seek(pt)
        docus=index.read(value*len_data)
        postin=struct.unpack(FORMAT_STRUCT.format(value),docus)

   

# print(os.path.getsize(dirname))

print("directory size",os.path.getsize(dirname))
print("directory posting",os.path.getsize("index.bin"))
print("directory index",os.path.getsize("voc.txt"))
print("---------------------------------------------")
print("overhead",((os.path.getsize("index.bin")-os.path.getsize("voc.txt")-os.path.getsize(dirname))/os.path.getsize("index.bin"))/os.path.getsize("index.bin"),"%")
#print("result",size_obj_index+sys.getsizeof(vocs)-os.path.getsize(dirname))
#print(vocs)


vocs.sort(key=operator.itemgetter(1))
distribution={}
befor_df=vocs[0][1]
aux=0
#print(befor_df)
for _,df,_ in vocs:
    if befor_df==df:
        aux+=1
    else:
        distribution[befor_df]=aux
        aux=1
        befor_df=df
#print(distribution)
# print(vocs)

plot_bar(distribution.values(),distribution.keys())
